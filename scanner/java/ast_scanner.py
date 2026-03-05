#!/usr/bin/env python3
"""
AST Scanner — Python wrapper for the Spoon-based Java AST engine.

Delegates all analysis to ast-engine.jar and normalizes the JSON output.
"""
import json
import subprocess
import argparse
import sys
from pathlib import Path
from typing import Optional


ENGINE_JAR = Path(__file__).parent / "ast-engine.jar"


def find_engine_jar(override: Optional[str] = None) -> Path:
    if override:
        jar = Path(override)
        if not jar.is_file():
            raise FileNotFoundError(f"Engine JAR not found: {jar}")
        return jar
    if not ENGINE_JAR.is_file():
        raise FileNotFoundError(
            f"ast-engine.jar not found at {ENGINE_JAR}. "
            "Build it first or pass --engine-jar."
        )
    return ENGINE_JAR


def build_engine_args(jar: Path, args) -> list[str]:
    cmd = ["java", "-jar", str(jar), "--source", args.source]
    if args.entrypoints:
        cmd += ["--entrypoints"] + args.entrypoints
    if args.depth is not None:
        cmd += ["--depth", str(args.depth)]
    if args.include_tests:
        cmd.append("--include-tests")
    if args.format:
        cmd += ["--format", args.format]
    return cmd


def run_engine(cmd: list[str]) -> dict:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return _error_result("Engine timed out after 120s")
    except FileNotFoundError:
        return _error_result("'java' not found. Ensure JDK is installed and on PATH.")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        return _error_result(f"Engine exited with code {result.returncode}: {stderr}")

    stdout = result.stdout.strip()
    if not stdout:
        return _error_result("Engine produced no output")

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        return _error_result(f"Failed to parse engine output as JSON: {e}", raw=stdout)


def _error_result(message: str, raw: str = "") -> dict:
    result = {
        "project": "",
        "entrypoints": [],
        "graph": {"nodes": [], "edges": []},
        "metadata": {"errors": [message]},
    }
    if raw:
        result["metadata"]["raw_output"] = raw[:2000]
    return result


def normalize(data: dict, source_path: str) -> dict:
    """Ensure required top-level keys exist."""
    data.setdefault("project", Path(source_path).name)
    data.setdefault("entrypoints", [])
    data.setdefault("graph", {"nodes": [], "edges": []})
    data.setdefault("metadata", {})
    data["metadata"].setdefault("errors", [])
    return data


def main():
    parser = argparse.ArgumentParser(
        description="AST Scanner — static analysis of Java source files via Spoon"
    )
    parser.add_argument("--source", required=True, help="Root directory of Java source files")
    parser.add_argument("--output", help="Path to write JSON output file")
    parser.add_argument("--entrypoints", nargs="*", help="Limit analysis to specific classes")
    parser.add_argument("--depth", type=int, help="Maximum call-graph traversal depth")
    parser.add_argument("--include-tests", action="store_true", help="Include test sources")
    parser.add_argument("--format", default="json", choices=["json"], help="Output format")
    parser.add_argument("--engine-jar", help="Path to ast-engine.jar (overrides default location)")

    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        print(f"ERROR: --source must be an existing directory: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        jar = find_engine_jar(args.engine_jar)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    cmd = build_engine_args(jar, args)
    result = run_engine(cmd)
    result = normalize(result, args.source)

    output_json = json.dumps(result, indent=2)

    if args.output:
        out = Path(args.output)
        if out.is_dir() or args.output.endswith("/"):
            out = out / f"{Path(args.source).name}-ast.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output_json)
        print(f"Output written to: {out}")
    else:
        print(output_json)

    errors = result.get("metadata", {}).get("errors", [])
    if errors:
        for err in errors:
            print(f"WARNING: {err}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
