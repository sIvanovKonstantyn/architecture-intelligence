`org.springframework.boot:spring-boot-configuration-processor` is a **compile-time annotation processor** provided by Spring Boot. Its main purpose is to **generate metadata for your `@ConfigurationProperties` classes**, which enables IDEs like IntelliJ IDEA or Eclipse to provide **code completion, validation, and documentation** for your configuration properties in `application.properties` or `application.yml`.

Here's a concise guide on how to use it:

---

## 1. Add Dependency

For **Maven**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-configuration-processor</artifactId>
    <optional>true</optional>
</dependency>
```

For **Gradle**:

```gradle
dependencies {
    annotationProcessor "org.springframework.boot:spring-boot-configuration-processor"
}
```

⚠️ Note: This is an **annotation processor**, not a runtime dependency. Mark it `optional` in Maven or use `annotationProcessor` in Gradle.

---

## 2. Create a `@ConfigurationProperties` Class

```java
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private String name;
    private int timeout;

    // getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getTimeout() { return timeout; }
    public void setTimeout(int timeout) { this.timeout = timeout; }
}
```

* `prefix = "app"` → maps `app.name` and `app.timeout` from `application.properties` or `application.yml`.

---

## 3. Use Properties in `application.yml` or `application.properties`

```yaml
app:
  name: MyApp
  timeout: 30
```

---

## 4. Benefits of Using the Configuration Processor

1. **IDE Support**:

   * Autocompletion in `application.yml`/`properties`.
   * Highlighting of invalid property names or types.

2. **Metadata Generation**:

   * Generates `META-INF/spring-configuration-metadata.json` during compilation.
   * Useful for Spring Boot tools and documentation.

3. **Validation**:

   * Works with `@Validated` and JSR-303 annotations (`@NotNull`, `@Min`, etc.) for configuration properties.

---

## 5. Optional: Add Validation

```java
import jakarta.validation.constraints.Min;
import org.springframework.validation.annotation.Validated;

@Component
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {

    private String name;

    @Min(1)
    private int timeout;

    // getters/setters
}
```

If you try to set `app.timeout: 0` in `application.yml`, Spring Boot will fail the startup with a validation error.

---

✅ **TL;DR**: `spring-boot-configuration-processor` **enhances developer experience** by generating metadata for your `@ConfigurationProperties` classes, giving IDEs autocompletion, validation, and documentation, without adding runtime overhead.

---