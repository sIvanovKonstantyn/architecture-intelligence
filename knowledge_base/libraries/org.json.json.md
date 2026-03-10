`org.json` is a popular lightweight Java library for parsing, creating, and manipulating JSON data. The core classes include `JSONObject` and `JSONArray`, which let you work with JSON objects and arrays in Java easily. It’s not part of the standard JDK, so you need to include it as a dependency (Maven, Gradle, or manually).

Here’s a short guide on how to use it:

---

### 1. Add Dependency

**Maven:**

```xml
<dependency>
    <groupId>org.json</groupId>
    <artifactId>json</artifactId>
    <version>20230227</version>
</dependency>
```

**Gradle:**

```gradle
implementation 'org.json:json:20230227'
```

---

### 2. Creating a JSON Object

```java
import org.json.JSONObject;

public class JsonExample {
    public static void main(String[] args) {
        JSONObject obj = new JSONObject();
        obj.put("name", "Alice");
        obj.put("age", 25);
        obj.put("active", true);

        System.out.println(obj.toString()); // {"name":"Alice","age":25,"active":true}
    }
}
```

---

### 3. Creating a JSON Array

```java
import org.json.JSONArray;

public class JsonArrayExample {
    public static void main(String[] args) {
        JSONArray array = new JSONArray();
        array.put("Java");
        array.put("Python");
        array.put("JavaScript");

        System.out.println(array.toString()); // ["Java","Python","JavaScript"]
    }
}
```

---

### 4. Parsing JSON from String

```java
String jsonString = "{\"name\":\"Bob\",\"age\":30}";
JSONObject obj = new JSONObject(jsonString);

String name = obj.getString("name"); // "Bob"
int age = obj.getInt("age");          // 30
```

---

### 5. Nested JSON Objects and Arrays

```java
JSONObject person = new JSONObject();
person.put("name", "Carol");
person.put("skills", new JSONArray().put("Java").put("SQL"));

JSONObject company = new JSONObject();
company.put("employee", person);

System.out.println(company.toString());
// {"employee":{"name":"Carol","skills":["Java","SQL"]}}
```

---

### 6. Useful Methods

* `obj.has("key")` — check if key exists
* `obj.remove("key")` — remove a key
* `obj.keySet()` — get all keys
* `array.length()` — get array size
* `array.get(index)` — get element at index

---

💡 **Tip:** `org.json` is simple and fast for small JSON tasks. For more complex JSON parsing (like mapping JSON to Java classes), consider **Jackson** or **Gson**.