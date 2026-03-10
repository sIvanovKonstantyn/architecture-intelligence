## `com.fasterxml.jackson.datatype:jackson-datatype-jsr310` — Short Guide

### 1. What is `jackson-datatype-jsr310`?

`jackson-datatype-jsr310` is a Jackson module that adds **JSON serialization and deserialization support for Java 8 Date and Time API** (JSR-310).

Without this module, Jackson Databind does **not properly handle classes from** JSR‑310 (Java Date and Time API) such as:

* `LocalDate`
* `LocalDateTime`
* `Instant`
* `OffsetDateTime`
* `ZonedDateTime`
* `Duration`

The module provides serializers and deserializers so these types can be converted **to and from JSON correctly**.

It is commonly used in applications built with frameworks like Spring Boot.

---

# 2. Dependency

### Maven

```xml
<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jsr310</artifactId>
    <version>2.17.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.17.0'
```

---

# 3. Registering the Module

To enable support for Java Time classes, register the module in `ObjectMapper`.

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());
```

The `JavaTimeModule` class is provided by the module.

---

# 4. Example: Serializing `LocalDate`

### Java class

```java
public class Event {
    public String name;
    public LocalDate date;
}
```

### Serialization

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());

Event event = new Event();
event.name = "Conference";
event.date = LocalDate.of(2026, 3, 7);

String json = mapper.writeValueAsString(event);
```

Output:

```json
{
  "name": "Conference",
  "date": "2026-03-07"
}
```

---

# 5. Example: Deserializing JSON

JSON:

```json
{
  "name": "Conference",
  "date": "2026-03-07"
}
```

Code:

```java
Event event = mapper.readValue(json, Event.class);
```

Jackson automatically converts the string to `LocalDate`.

---

# 6. Handling `LocalDateTime`

Example class:

```java
public class Order {
    public long id;
    public LocalDateTime createdAt;
}
```

Serialization result:

```json
{
  "id": 1,
  "createdAt": "2026-03-07T10:15:30"
}
```

---

# 7. Avoiding Timestamp Format

By default, Jackson may serialize dates as **timestamps**.

Disable this behavior:

```java
mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
```

Example configuration:

```java
ObjectMapper mapper = new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
```

This ensures dates appear as **ISO-8601 strings**, which is the standard format used in APIs.

---

# 8. Custom Date Formats

You can customize formatting using annotations.

Example:

```java
public class Event {

    public String name;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm")
    public LocalDateTime time;
}
```

Example JSON:

```json
{
  "name": "Meeting",
  "time": "2026-03-07 14:30"
}
```

Annotations come from Jackson Annotations.

---

# 9. Spring Boot Integration

In modern versions of Spring Boot, this module is usually **auto-configured** if it is present on the classpath.

Typical configuration:

```java
@Bean
ObjectMapper objectMapper() {
    return JsonMapper.builder()
        .addModule(new JavaTimeModule())
        .build();
}
```

---

# 10. Supported Java Time Types

Commonly supported classes include:

| Type             | Example JSON                                 |
| ---------------- | -------------------------------------------- |
| `LocalDate`      | `"2026-03-07"`                               |
| `LocalDateTime`  | `"2026-03-07T10:15:30"`                      |
| `Instant`        | `"2026-03-07T09:15:30Z"`                     |
| `OffsetDateTime` | `"2026-03-07T10:15:30+01:00"`                |
| `ZonedDateTime`  | `"2026-03-07T10:15:30+01:00[Europe/Zagreb]"` |

---

# 11. When to Use This Module

You should include `jackson-datatype-jsr310` whenever your models use **Java Time API types**.

Typical cases:

* REST APIs
* event timestamps
* scheduling systems
* audit logs
* domain models using `java.time`

---

✅ **Summary**

`jackson-datatype-jsr310` adds support for **Java 8+ date/time types** to the Jackson JSON ecosystem.

It enables:

```
LocalDate / LocalDateTime / Instant
          ↓
      JSON ISO-8601
```

The module integrates with:

* Jackson Databind
* Spring Boot

and is essential for modern Java applications that use the **Java Time API**.