#!/usr/bin/env python3
import json
import re
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Optional

class RestScanner:
    REST_ANNOTATIONS = {'RestController', 'Controller'}
    HTTP_METHODS = {
        'GetMapping': 'GET',
        'PostMapping': 'POST',
        'PutMapping': 'PUT',
        'DeleteMapping': 'DELETE',
        'PatchMapping': 'PATCH',
        'RequestMapping': 'REQUEST'
    }
    EXCLUDE_DIRS = {'test', 'generated', '.git'}

    def __init__(self, repo_path: str, output_dir: str, exclude_folders: Optional[List[str]] = None):
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir)
        self.exclude_folders = set(exclude_folders or []) | self.EXCLUDE_DIRS
        self.javap_dir = self.output_dir / 'javap_output'
        self.javap_dir.mkdir(parents=True, exist_ok=True)
        self.dto_cache = {}
        self.dto_search_root = self._find_classes_root()

    def _find_classes_root(self) -> Path:
        """Walk up from repo_path to find target/classes directory."""
        for parent in [self.repo_path, *self.repo_path.parents]:
            if parent.name == 'classes' and parent.parent.name == 'target':
                return parent
        return self.repo_path

    def scan(self) -> Dict:
        controllers = []
        for class_file in self._find_class_files():
            if controller := self._parse_controller(class_file):
                controllers.append(controller)
        
        return {
            "service_name": self.repo_path.name,
            "language": "java",
            "frameworks_detected": ["spring-boot"] if controllers else [],
            "controllers": controllers
        }

    def _find_class_files(self):
        for path in self.repo_path.rglob("*.class"):
            if not any(ex in path.parts for ex in self.exclude_folders):
                yield path

    def _parse_controller(self, file_path: Path) -> Optional[Dict]:
        javap_output = self._run_javap(file_path)
        
        if not any(ann in javap_output for ann in self.REST_ANNOTATIONS):
            return None

        class_name = self._extract_class_name(javap_output)
        
        # Save javap output to file
        javap_file = self.javap_dir / f"{class_name}.javap"
        javap_file.write_text(javap_output)

        base_path = self._extract_base_path(javap_output)
        methods = self._extract_methods(javap_output, class_name)

        return {
            "class": class_name,
            "base_path": base_path,
            "methods": methods
        } if methods else None

    def _run_javap(self, class_file: Path) -> str:
        try:
            result = subprocess.run(
                ['javap', '-v', '-private', str(class_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception:
            return ""

    def _extract_class_name(self, content: str) -> str:
        match = re.search(r'SourceFile:\s*"([^"]+)\.java"', content)
        if match:
            return match.group(1)
        return "Unknown"

    def _extract_base_path(self, content: str) -> str:
        pattern = r'org\.springframework\.web\.bind\.annotation\.RequestMapping\([^)]*value=\["([^"]+)"\]'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        return ""

    def _extract_methods(self, content: str, class_name: str = "") -> List[Dict]:
        methods = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            # Look for RuntimeVisibleAnnotations that are NOT at class level
            if 'RuntimeVisibleAnnotations:' in lines[i]:
                # Check if this is NOT the class-level annotation (appears before first method)
                # Class-level appears before the opening brace of the class
                if i > 0 and not any('SourceFile:' in lines[j] for j in range(max(0, i-10), i)):
                    # This is a method-level annotation
                    annotation_start = i
                    annotation_lines = []
                    i += 1
                    
                    # Collect annotation block
                    while i < len(lines) and (lines[i].startswith('      ') or lines[i].strip() == ''):
                        annotation_lines.append(lines[i])
                        i += 1
                    
                    annotation_block = '\n'.join(annotation_lines)
                    
                    # Check for HTTP method annotations
                    for annotation in self.HTTP_METHODS:
                        if annotation in annotation_block:
                            http_method = self.HTTP_METHODS[annotation]
                            path = self._extract_method_path(annotation_block, annotation) or "/"
                            
                            if annotation == 'RequestMapping':
                                http_method = self._extract_request_method(annotation_block) or 'GET'
                            
                            # Find method signature for input/output
                            method_sig = self._find_method_signature(content, annotation_start)
                            input_dto = self._extract_input_dto(method_sig)
                            output_dto = self._extract_output_dto(method_sig)
                            
                            methods.append({
                                "http_method": http_method,
                                "path": path,
                                "input": input_dto,
                                "output": output_dto
                            })
                            break
                else:
                    i += 1
            else:
                i += 1
        
        return methods
    
    def _find_method_signature(self, content: str, annotation_line: int) -> str:
        lines = content.split('\n')
        # Signature appears BEFORE RuntimeVisibleAnnotations in javap output
        for i in range(annotation_line, max(0, annotation_line - 50), -1):
            if 'Signature:' in lines[i]:
                match = re.search(r'Signature:.*?//\s*(.+)', lines[i])
                if match:
                    return match.group(1).strip()
        return ""
    
    def _extract_input_dto(self, method_sig: str) -> Optional[Dict]:
        # Extract parameter type from Signature line
        # Format: (Lcom/package/ClassName;)Lreturn/Type;
        match = re.search(r'\(L([^;)]+);', method_sig)
        if match:
            class_path = match.group(1).replace('/', '.')
            return self._get_dto_fields(class_path)
        return None
    
    def _extract_output_dto(self, method_sig: str) -> Optional[Dict]:
        # Extract return type from Signature line, handling generics
        # Format: )Lorg/springframework/http/ResponseEntity<Lcom/package/Response;>;
        # Look for type inside ResponseEntity<...>
        match = re.search(r'ResponseEntity<L([^;<>]+);', method_sig)
        if match:
            class_path = match.group(1).replace('/', '.')
            # Skip collections
            if not any(skip in class_path for skip in ['java.util.List', 'java.util.Set', 'java.util.Map', 'java.lang']):
                return self._get_dto_fields(class_path)
        
        # If no ResponseEntity, look for direct return type
        match = re.search(r'\)[^L]*L([^;<]+);', method_sig)
        if match:
            class_path = match.group(1).replace('/', '.')
            if 'ResponseEntity' not in class_path and not any(skip in class_path for skip in ['java.util', 'java.lang']):
                return self._get_dto_fields(class_path)
        
        return None
    
    def _get_dto_fields(self, class_path: str) -> Optional[Dict]:
        # Check cache
        if class_path in self.dto_cache:
            return self.dto_cache[class_path]
        
        # Skip primitive types and common classes
        if any(skip in class_path for skip in ['java/', 'String', 'Integer', 'Long', 'Boolean', 'List', 'Set', 'Map']):
            return None
        
        class_name = class_path.split('.')[-1]
        
        # Find the class file
        class_file = self._find_class_file(class_path)
        if not class_file:
            result = {"class": class_name, "fields": []}
            self.dto_cache[class_path] = result
            return result
        
        # Run javap and extract fields
        javap_output = self._run_javap(class_file)
        
        # Save DTO javap output
        (self.javap_dir / f"{class_name}.javap").write_text(javap_output)
        
        fields = self._extract_dto_fields_from_javap(javap_output)
        
        result = {"class": class_name, "fields": fields}
        self.dto_cache[class_path] = result
        return result
    
    def _find_class_file(self, class_path: str) -> Optional[Path]:
        file_path = class_path.replace('.', '/') + '.class'
        for path in self.dto_search_root.rglob(file_path):
            if not any(ex in path.parts for ex in self.exclude_folders):
                return path
        return None
    
    def _extract_dto_fields_from_javap(self, content: str) -> List[Dict]:
        fields = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Look for private fields (typical DTO pattern)
            if line.strip().startswith('private ') and ';' in line:
                match = re.search(r'private\s+([\w.<>\[\]]+)\s+(\w+);', line)
                if match:
                    field_type = match.group(1)
                    field_name = match.group(2)
                    # Skip static/final fields
                    if 'static' not in line and 'final' not in line:
                        fields.append({
                            "name": field_name,
                            "type": self._simplify_type(field_type)
                        })
        
        return fields
    
    def _simplify_type(self, java_type: str) -> str:
        # Simplify Java types for readability
        type_map = {
            'Ljava/lang/String;': 'String',
            'Ljava/lang/Integer;': 'Integer',
            'Ljava/lang/Long;': 'Long',
            'Ljava/lang/Boolean;': 'Boolean',
            'Ljava/util/List': 'List',
            'Ljava/util/Set': 'Set',
            'Ljava/util/Map': 'Map'
        }
        
        for pattern, simple in type_map.items():
            if pattern in java_type:
                return simple
        
        # Extract simple class name
        if '/' in java_type:
            return java_type.split('/')[-1].replace(';', '')
        
        return java_type

    def _extract_method_path(self, block: str, annotation: str) -> Optional[str]:
        # Look for full annotation path with value=["path"] format
        pattern = rf'org\.springframework\.web\.bind\.annotation\.{annotation}\([^)]*(?:value|path)=\["([^"]+)"\]'
        match = re.search(pattern, block, re.DOTALL)
        if match:
            return match.group(1)
        
        # Look for jakarta annotation
        pattern = rf'jakarta\.ws\.rs\.{annotation}\([^)]*(?:value|path)=\["([^"]+)"\]'
        match = re.search(pattern, block, re.DOTALL)
        if match:
            return match.group(1)
        
        return None

    def _extract_request_method(self, block: str) -> Optional[str]:
        match = re.search(r'RequestMethod\.(\w+)', block)
        return match.group(1) if match else None

def main():
    parser = argparse.ArgumentParser(description='Scan Java REST controllers')
    parser.add_argument('--repo-path', required=True, help='Repository root path')
    parser.add_argument('--output', required=True, help='Output directory path')
    parser.add_argument('--exclude-folders', nargs='*', help='Folders to exclude')
    parser.add_argument('--keep-tmp', action='store_true', help='Keep javap tmp files after scanning')
    
    args = parser.parse_args()
    
    scanner = RestScanner(args.repo_path, args.output, args.exclude_folders)
    result = scanner.scan()
    
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    output_file = output_path / f"{result['service_name']}-rest.json"
    output_file.write_text(json.dumps(result, indent=2))
    
    if not args.keep_tmp:
        import shutil
        shutil.rmtree(scanner.javap_dir, ignore_errors=True)
    
    print(f"Scan complete. Output: {output_file}")


if __name__ == "__main__":
    main()
