## `com.fasterxml.jackson.core:jackson-databind` — Short Guide

### 1. What is `jackson-databind`?

`jackson-databind` is the **high-level data-binding module** of the Jackson JSON Processor ecosystem.

It allows you to **convert between JSON and Java objects (POJOs)** automatically.

This module builds on top of:

* Jackson Core — low-level JSON streaming API
* Jackson Annotations — configuration annotations

The main class provided by `jackson-databind` is:

```
ObjectMapper
```

`ObjectMapper` handles:

* JSON → Java objects (deserialization)
* Java objects → JSON (serialization)
* configuration and customization

---

# 2. Dependency

### Maven

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.17.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'com.fasterxml.jackson.core:jackson-databind:2.17.0'
```

---

# 3. Core Concept — `ObjectMapper`

`ObjectMapper` is the central API for working with JSON.

```java
ObjectMapper mapper = new ObjectMapper();
```

Typical operations:

| Operation            | Method                 |
| -------------------- | ---------------------- |
| JSON → Object        | `readValue()`          |
| Object → JSON        | `writeValue()`         |
| Object → JSON String | `writeValueAsString()` |

---

# 4. Serializing Java Objects to JSON

### Example Java class

```java
public class User {
    public String name;
    public int age;
}
```

### Serialize to JSON

```java
ObjectMapper mapper = new ObjectMapper();

User user = new User();
user.name = "Alice";
user.age = 30;

String json = mapper.writeValueAsString(user);

System.out.println(json);
```

Output:

```json
{"name":"Alice","age":30}
```

You can also write directly to a file:

```java
mapper.writeValue(new File("user.json"), user);
```

---

# 5. Deserializing JSON to Java Objects

Example JSON:

```json
{
  "name": "Alice",
  "age": 30
}
```

### Convert to Java object

```java
ObjectMapper mapper = new ObjectMapper();

User user = mapper.readValue(jsonString, User.class);

System.out.println(user.name);
```

Jackson automatically maps JSON fields to class fields.

---

# 6. Working with Collections

### Deserialize JSON array

JSON:

```json
[
  {"name":"Alice","age":30},
  {"name":"Bob","age":25}
]
```

Example:

```java
List<User> users = mapper.readValue(
    json,
    new TypeReference<List<User>>() {}
);
```

---

# 7. Using Jackson Annotations

Annotations allow customization of serialization/deserialization.

Provided by Jackson Annotations.

### Ignore fields

```java
public class User {

    public String name;

    @JsonIgnore
    public String password;
}
```

### Rename JSON fields

```java
public class User {

    @JsonProperty("user_name")
    public String name;
}
```

---

# 8. Pretty Printing JSON

To generate readable JSON:

```java
String json = mapper
    .writerWithDefaultPrettyPrinter()
    .writeValueAsString(user);
```

Output:

```json
{
  "name" : "Alice",
  "age" : 30
}
```

---

# 9. Mapping JSON without POJOs

You can also work with **dynamic JSON structures**.

Example:

```java
JsonNode node = mapper.readTree(json);

String name = node.get("name").asText();
```

`JsonNode` is useful when:

* JSON structure is unknown
* you need flexible parsing

---

# 10. Performance Tips

### Reuse `ObjectMapper`

`ObjectMapper` is **thread-safe after configuration**.

Create it once:

```java
@Bean
public ObjectMapper objectMapper() {
    return new ObjectMapper();
}
```

This is the common pattern in frameworks like
Spring Boot.

---

# 11. Common Use Cases

`jackson-databind` is widely used for:

* REST APIs
* JSON configuration files
* message serialization
* data integration pipelines

It is also used internally by frameworks like:

* Spring Boot
* HAPI FHIR

---

# 12. When to Use `jackson-databind`

Use `jackson-databind` when you want:

✔ simple POJO ↔ JSON conversion
✔ minimal boilerplate
✔ flexible configuration via annotations

Avoid it when:

* processing **huge JSON streams**
* building **low-level libraries**

In those cases use:

* Jackson Core.

---

✅ **Summary**

`jackson-databind` is the **high-level JSON mapping library** in the Jackson ecosystem.
It provides the powerful `ObjectMapper` API to convert between:

```
Java Objects ↔ JSON
```

It is the **most commonly used Jackson module** and is the default JSON engine in many Java frameworks.