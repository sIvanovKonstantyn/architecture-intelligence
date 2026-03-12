# Java REST Scanner

Scans compiled Java `.class` files to extract REST controller metadata using `javap` bytecode inspection.

## Requirements

- Python 3.8+
- `javap` (included with JDK)

## Usage

```bash
python rest_scanner.py \
  --repo-path <path-to-classes> \
  --output <output-dir> \
  [--exclude-folders <folder1> <folder2>] \
  [--keep-tmp]
```

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `--repo-path` | ✅ | Path to the compiled `.class` files to scan for controllers |
| `--output` | ✅ | Directory where the result JSON and optional javap files are saved |
| `--exclude-folders` | ❌ | Space-separated folder names to exclude (e.g. `test generated`) |
| `--keep-tmp` | ❌ | Keep intermediate `javap_output/` files after scanning (default: deleted) |

---

# Java AST Scanner

Scans Java source files to extract call graphs and transaction flows using [Spoon](https://spoon.gforge.inria.fr/) static analysis.

## Requirements

- Python 3.8+
- Java 17+
- Maven (to build from source)

## Build from Source

```bash
cd ast-engine
mvn package -q
cp target/ast-engine.jar ../ast-engine.jar
```

This produces `ast-engine.jar` in the `scanner/java/` directory, which `ast_scanner.py` uses by default.

## Usage

```bash
python ast_scanner.py \
  --source <path-to-java-sources> \
  --output <output-file-or-dir> \
  [--entrypoints <Class1> <Class2>] \
  [--depth <n>] \
  [--include-tests] \
  [--engine-jar <path-to-jar>]
```

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `--source` | ✅ | Root directory of Java source files to analyse |
| `--output` | ❌ | File or directory to write JSON output (prints to stdout if omitted) |
| `--entrypoints` | ❌ | Limit analysis to specific classes (space-separated) |
| `--depth` | ❌ | Maximum call-graph traversal depth |
| `--include-tests` | ❌ | Include test source files in analysis |
| `--engine-jar` | ❌ | Path to `ast-engine.jar` (overrides default location) |

## Example

```bash
python ast_scanner.py \
  --source /projects/my-service/src/main/java \
  --output /tmp/scan-results \
  --entrypoints com.example.OrderService \
  --depth 5
```

## Output Format

```json
{
  "project": "my-service",
  "entrypoints": ["com.example.OrderService"],
  "graph": {
    "nodes": [
      { "id": "com.example.OrderService.createOrder", "type": "method" }
    ],
    "edges": [
      { "from": "com.example.OrderService.createOrder", "to": "com.example.PaymentService.charge" }
    ]
  },
  "metadata": {
    "errors": []
  }
}
```

---

# Java Libs KB Parser

Parses a Maven `pom.xml` to extract dependencies and scaffolds a knowledge base directory with one Markdown stub per library.

## Requirements

- Python 3.8+

## Usage

```bash
python libs_kb_parser.py <pom.xml> <kb_dir>
```

## Parameters

| Parameter | Description |
|---|---|
| `pom.xml` | Path to the Maven POM file to parse |
| `kb_dir` | Directory where Markdown stubs will be created |

## Example

```bash
python libs_kb_parser.py /projects/my-service/pom.xml /tmp/kb
```

For each dependency found, a file named `<groupId>.<artifactId>.md` is created in `kb_dir` with a short prompt asking for a usage guide. Already-existing files are skipped.

---

# Java REST Scanner

## Notes

- `--repo-path` should point to the controller classes directory (e.g. `target/classes/com/example/rest`)
- DTO classes are searched from `target/classes` upward, so all packages are covered
- Output file is named `<service_name>-rest.json` inside `--output`

## Example

```bash
python rest_scanner.py \
  --repo-path /projects/my-service/target/classes/com/example/rest \
  --output /tmp/scan-results \
  --exclude-folders test generated \
  --keep-tmp
```

## Output Format

```json
{
  "service_name": "my-service",
  "language": "java",
  "frameworks_detected": ["spring-boot"],
  "controllers": [
    {
      "class": "UserController",
      "base_path": "/api/v1/users",
      "methods": [
        {
          "http_method": "POST",
          "path": "/",
          "input": {
            "class": "CreateUserRequest",
            "fields": [
              { "name": "email", "type": "java.lang.String" }
            ]
          },
          "output": {
            "class": "CreateUserResponse",
            "fields": [
              { "name": "id", "type": "java.lang.String" }
            ]
          }
        }
      ]
    }
  ]
}
```
