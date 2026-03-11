import json
import glob
import argparse
from pathlib import Path


def load_service_files(input_dir: str) -> dict[str, Path]:
    """Returns a map of service_name -> file path for all *-http-dependencies.json files."""
    files = glob.glob(str(Path(input_dir) / "*-http-dependencies.json"))
    service_map = {}
    for f in files:
        with open(f) as fh:
            data = json.load(fh)
        service_map[data["service"]] = (f, data)
    return service_map


def build_graph(input_dir: str) -> dict:
    service_map = load_service_files(input_dir)
    graph = {}  # service -> set of dependencies
    analyzed = set()

    def analyze(service_name: str, data: dict):
        if service_name in analyzed:
            return
        analyzed.add(service_name)
        deps = set()
        for dep in data.get("dependencies", []):
            target = dep.get("targetService")
            if not target:
                continue
            deps.add(target)
            if target not in analyzed and target in service_map:
                _, target_data = service_map[target]
                analyze(target, target_data)
        graph[service_name] = sorted(deps)

    for service_name, (_, data) in service_map.items():
        analyze(service_name, data)

    return graph


def main():
    parser = argparse.ArgumentParser(description="Build service dependency graph from HTTP dependency files.")
    parser.add_argument("input_dir", help="Directory containing *-http-dependencies.json files")
    args = parser.parse_args()

    graph = build_graph(args.input_dir)

    output_path = Path(args.input_dir) / "service-graph.json"
    with open(output_path, "w") as f:
        json.dump(graph, f, indent=2)

    print(f"Graph written to {output_path}")
    for service, deps in graph.items():
        print(f"  {service} -> {deps if deps else '[]'}")


if __name__ == "__main__":
    main()
