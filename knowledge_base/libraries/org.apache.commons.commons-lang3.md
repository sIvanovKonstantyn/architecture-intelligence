**`org.apache.commons:commons-lang3`** is a utility library from the Apache Software Foundation that provides **helper methods for working with core Java classes** such as `String`, `Object`, `Number`, `Array`, `Reflection`, and `Concurrency`.

It extends the functionality of the Java standard library and removes a lot of **boilerplate code**.

Typical usage includes:

* null-safe operations
* string manipulation
* object comparison
* reflection helpers
* random utilities
* builders for `equals`, `hashCode`, and `toString`

---

# 1. Dependency

### Maven

```xml
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>3.14.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.apache.commons:commons-lang3:3.14.0'
```

---

# 2. Key Utility Classes

| Class               | Purpose                       |
| ------------------- | ----------------------------- |
| `StringUtils`       | String utilities              |
| `ObjectUtils`       | Null-safe object operations   |
| `ArrayUtils`        | Array helpers                 |
| `NumberUtils`       | Number parsing and validation |
| `RandomStringUtils` | Random strings                |
| `ReflectionUtils`   | Reflection helpers            |
| `Validate`          | Runtime validation            |
| `EqualsBuilder`     | Simplify `equals()`           |
| `HashCodeBuilder`   | Simplify `hashCode()`         |
| `ToStringBuilder`   | Simplify `toString()`         |

---

# 3. String Utilities (`StringUtils`)

One of the most used parts of the library.

### Null-safe checks

```java
import org.apache.commons.lang3.StringUtils;

StringUtils.isEmpty(null);      // true
StringUtils.isEmpty("");        // true
StringUtils.isBlank("   ");     // true
StringUtils.isNotBlank("abc");  // true
```

Difference:

| Method      | Meaning            |
| ----------- | ------------------ |
| `isEmpty()` | null or ""         |
| `isBlank()` | null or whitespace |

---

### Default values

```java
String value = StringUtils.defaultIfBlank(input, "default");
```

---

### Joining strings

```java
String result = StringUtils.join(List.of("A", "B", "C"), ",");
// A,B,C
```

---

### String comparison (null-safe)

```java
StringUtils.equals(a, b);
StringUtils.equalsIgnoreCase(a, b);
```

---

# 4. Object Utilities (`ObjectUtils`)

Null-safe object handling.

```java
import org.apache.commons.lang3.ObjectUtils;

ObjectUtils.defaultIfNull(value, "fallback");
```

Example:

```java
String result = ObjectUtils.defaultIfNull(name, "Unknown");
```

---

# 5. Array Utilities (`ArrayUtils`)

Working with arrays.

```java
import org.apache.commons.lang3.ArrayUtils;

int[] arr = {1,2,3};

arr = ArrayUtils.add(arr, 4);

boolean contains = ArrayUtils.contains(arr, 2);
```

Convert array types:

```java
Integer[] boxed = ArrayUtils.toObject(new int[]{1,2,3});
```

---

# 6. Number Utilities (`NumberUtils`)

Safe number parsing.

```java
import org.apache.commons.lang3.math.NumberUtils;

int value = NumberUtils.toInt("123", 0); // default if invalid
```

Validation:

```java
NumberUtils.isCreatable("123.45"); // true
NumberUtils.isDigits("123");       // true
```

---

# 7. Random String Generation

```java
import org.apache.commons.lang3.RandomStringUtils;

String token = RandomStringUtils.randomAlphanumeric(16);
```

Examples:

```java
RandomStringUtils.randomAlphabetic(10);
RandomStringUtils.randomNumeric(6);
```

---

# 8. Validation (`Validate`)

Useful for method preconditions.

```java
import org.apache.commons.lang3.Validate;

Validate.notNull(user, "User must not be null");
Validate.isTrue(age > 0, "Age must be positive");
```

Equivalent to manual checks but shorter.

---

# 9. Builders for `equals`, `hashCode`, `toString`

### equals()

```java
import org.apache.commons.lang3.builder.EqualsBuilder;

@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User)) return false;

    User other = (User) o;

    return new EqualsBuilder()
            .append(id, other.id)
            .append(name, other.name)
            .isEquals();
}
```

---

### hashCode()

```java
import org.apache.commons.lang3.builder.HashCodeBuilder;

@Override
public int hashCode() {
    return new HashCodeBuilder()
            .append(id)
            .append(name)
            .toHashCode();
}
```

---

### toString()

```java
import org.apache.commons.lang3.builder.ToStringBuilder;

@Override
public String toString() {
    return new ToStringBuilder(this)
            .append("id", id)
            .append("name", name)
            .toString();
}
```

---

# 10. Pair and Triple

Useful lightweight data structures.

```java
import org.apache.commons.lang3.tuple.Pair;

Pair<String, Integer> pair = Pair.of("BTC", 60000);

pair.getLeft();
pair.getRight();
```

---

# 11. Common Real-World Usage

`commons-lang3` is commonly used for:

* removing repetitive null checks
* string validation
* random tokens and IDs
* DTO utility operations
* simplifying `equals/hashCode/toString`

It is widely used in frameworks such as:

* Spring Framework
* Apache Hadoop
* Apache Camel

---

✅ **Summary**

`commons-lang3` is one of the most widely used Java utility libraries. It provides **hundreds of helper methods for common programming tasks**, making Java code shorter, safer, and easier to read.