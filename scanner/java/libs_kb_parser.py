import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_dependencies(pom_path: str) -> list[tuple[str, str]]:
    tree = ET.parse(pom_path)
    root = tree.getroot()
    ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
    prefix = f"{{{ns}}}" if ns else ""

    deps = []
    for dep in root.iter(f"{prefix}dependency"):
        group = dep.find(f"{prefix}groupId")
        artifact = dep.find(f"{prefix}artifactId")
        if group is not None and artifact is not None:
            deps.append((group.text, artifact.text))
    return deps


def populate_kb(dependencies: list[tuple[str, str]], kb_dir: str):
    kb_path = Path(kb_dir)
    kb_path.mkdir(parents=True, exist_ok=True)

    for group, artifact in dependencies:
        name = f"{group}.{artifact}"
        md_file = kb_path / f"{name}.md"
        if not md_file.exists():
            md_file.write_text(f"what is {name}? write a short guide about how to use it.\n")
            print(f"created: {md_file}")
        else:
            print(f"skipped: {md_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: libs_kb_parser.py <pom.xml> <kb_dir>")
        sys.exit(1)

    deps = parse_dependencies(sys.argv[1])
    populate_kb(deps, sys.argv[2])
