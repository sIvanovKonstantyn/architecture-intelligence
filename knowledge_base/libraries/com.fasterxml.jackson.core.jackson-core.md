## `com.fasterxml.jackson.core:jackson-core` — Short Guide

### 1. What is `jackson-core`?

`jackson-core` is the **low-level streaming API** of the Jackson JSON Processor.
It provides the fundamental classes for **reading and writing JSON efficiently**.

Unlike higher-level modules such as:

* Jackson Databind (`ObjectMapper`)
* Jackson Annotations

`jackson-core` works directly with **JSON tokens**, making it extremely **fast and memory efficient**.

It is commonly used when:

* Processing **very large JSON documents**
* Building **custom serializers/deserializers**
* Implementing **high-performance data pipelines**
* Writing libraries that depend on JSON but should **not depend on databind**

---

# 2. Dependency

### Maven

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.17.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'com.fasterxml.jackson.core:jackson-core:2.17.0'
```

---

# 3. Core Concepts

The streaming API is built around two main classes:

| Class           | Purpose                    |
| --------------- | -------------------------- |
| `JsonParser`    | Reads JSON token-by-token  |
| `JsonGenerator` | Writes JSON token-by-token |

Both are created from a **`JsonFactory`**.

```java
JsonFactory factory = new JsonFactory();
```

---

# 4. Reading JSON (Streaming Parsing)

Example JSON:

```json
{
  "name": "Alice",
  "age": 30
}
```

### Example

```java
JsonFactory factory = new JsonFactory();

try (JsonParser parser = factory.createParser(jsonInputStream)) {

    while (parser.nextToken() != null) {
        String fieldName = parser.getCurrentName();

        if ("name".equals(fieldName)) {
            parser.nextToken();
            String name = parser.getValueAsString();
            System.out.println(name);
        }

        if ("age".equals(fieldName)) {
            parser.nextToken();
            int age = parser.getIntValue();
            System.out.println(age);
        }
    }
}
```

### How it works

Parser moves through **JSON tokens**:

```
START_OBJECT
FIELD_NAME (name)
VALUE_STRING (Alice)
FIELD_NAME (age)
VALUE_NUMBER_INT (30)
END_OBJECT
```

This approach avoids loading the entire JSON into memory.

---

# 5. Writing JSON (Streaming Generation)

Example using `JsonGenerator`.

```java
JsonFactory factory = new JsonFactory();

try (JsonGenerator generator = factory.createGenerator(System.out)) {

    generator.writeStartObject();

    generator.writeStringField("name", "Alice");
    generator.writeNumberField("age", 30);

    generator.writeEndObject();
}
```

Output:

```json
{"name":"Alice","age":30}
```

---

# 6. Processing Large JSON Files

Streaming is ideal for huge files.

Example: processing a large array.

```json
[
  {"id":1},
  {"id":2},
  {"id":3}
]
```

Example code:

```java
try (JsonParser parser = factory.createParser(file)) {

    while (parser.nextToken() != JsonToken.END_ARRAY) {

        if (parser.currentToken() == JsonToken.START_OBJECT) {

            int id = 0;

            while (parser.nextToken() != JsonToken.END_OBJECT) {
                String field = parser.getCurrentName();

                if ("id".equals(field)) {
                    parser.nextToken();
                    id = parser.getIntValue();
                }
            }

            processId(id);
        }
    }
}
```

This allows you to process **GB-sized JSON files** with constant memory.

---

# 7. Common Use Cases

### 1️⃣ High-performance JSON pipelines

Streaming avoids object creation overhead.

### 2️⃣ Custom libraries

Libraries often depend only on `jackson-core` to avoid heavy dependencies.

### 3️⃣ Big data processing

Handling large JSON logs or data exports.

### 4️⃣ Implementing custom serialization

Frameworks often build on top of `JsonParser` and `JsonGenerator`.

---

# 8. When to Use `jackson-core` vs `jackson-databind`

| Feature      | jackson-core | jackson-databind |
| ------------ | ------------ | ---------------- |
| Performance  | ⭐⭐⭐⭐⭐        | ⭐⭐⭐              |
| Memory usage | Low          | Higher           |
| Ease of use  | Harder       | Very easy        |
| POJO mapping | ❌            | ✅                |
| Streaming    | ✅            | Limited          |

Typical rule:

* **Application code → use `ObjectMapper`**
* **Framework / large data → use `jackson-core`**

---

# 9. Best Practices

### Use try-with-resources

```java
try (JsonParser parser = factory.createParser(file)) {
}
```

### Reuse `JsonFactory`

It is **thread-safe** and should usually be a singleton.

### Avoid manual parsing unless needed

If performance is not critical, prefer:

```java
ObjectMapper mapper = new ObjectMapper();
```

---

# 10. Typical Architecture in Jackson

```
Jackson Ecosystem

jackson-core
     ↓
jackson-databind
     ↓
Spring / REST / APIs
```

Many frameworks such as Spring Boot internally rely on these libraries for JSON serialization.

---

✅ **Summary**

`jackson-core` is the **low-level JSON streaming engine** of Jackson.
It provides:

* `JsonParser` — streaming JSON reader
* `JsonGenerator` — streaming JSON writer
* extremely **fast and memory-efficient JSON processing**

It is most useful for:

* large JSON files
* high-performance pipelines
* building libraries or frameworks.