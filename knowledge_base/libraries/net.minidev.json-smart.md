## What is `net.minidev:json-smart`

`net.minidev:json-smart` is a **lightweight JSON library for Java** that provides:

* JSON parsing and serialization
* Simple object model (`JSONObject`, `JSONArray`)
* Fast and low-dependency implementation
* Integration with libraries like **JSON‑Smart**, **JSON‑Path**, and **Nimbus JOSE + JWT**

It is commonly used internally by frameworks that need a **small JSON parser without the overhead of larger libraries** such as **Jackson** or **Gson**.

Package:

```
net.minidev:json-smart
```

---

# Adding the Dependency

### Maven

```xml
<dependency>
    <groupId>net.minidev</groupId>
    <artifactId>json-smart</artifactId>
    <version>2.5.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'net.minidev:json-smart:2.5.0'
```

---

# Core Classes

| Class        | Purpose           |
| ------------ | ----------------- |
| `JSONObject` | JSON object       |
| `JSONArray`  | JSON array        |
| `JSONParser` | Parse JSON string |
| `JSONValue`  | Utility methods   |

---

# 1. Parse JSON

```java
import net.minidev.json.JSONObject;
import net.minidev.json.parser.JSONParser;

String json = "{\"name\":\"Alice\",\"age\":30}";

JSONParser parser = new JSONParser(JSONParser.MODE_PERMISSIVE);
JSONObject obj = (JSONObject) parser.parse(json);

String name = (String) obj.get("name");
Long age = (Long) obj.get("age");

System.out.println(name + " " + age);
```

Key points:

* Parser modes control strictness.
* Numbers are often parsed as `Long` or `Double`.

---

# 2. Creating JSON

```java
import net.minidev.json.JSONObject;

JSONObject obj = new JSONObject();
obj.put("name", "Alice");
obj.put("age", 30);

String json = obj.toJSONString();

System.out.println(json);
```

Output:

```
{"name":"Alice","age":30}
```

---

# 3. Working with Arrays

```java
import net.minidev.json.JSONArray;

JSONArray arr = new JSONArray();
arr.add("BTC");
arr.add("ETH");
arr.add("SOL");

System.out.println(arr.toJSONString());
```

Output:

```
["BTC","ETH","SOL"]
```

---

# 4. Parsing Nested JSON

```java
String json = """
{
  "user": {
    "name": "Alice",
    "roles": ["admin","user"]
  }
}
""";

JSONParser parser = new JSONParser();
JSONObject root = (JSONObject) parser.parse(json);

JSONObject user = (JSONObject) root.get("user");
JSONArray roles = (JSONArray) user.get("roles");

System.out.println(user.get("name"));
System.out.println(roles.get(0));
```

---

# 5. Quick Parsing with `JSONValue`

Shortcut API:

```java
import net.minidev.json.JSONValue;

JSONObject obj = (JSONObject) JSONValue.parse("{\"a\":1}");
System.out.println(obj.get("a"));
```

---

# Parser Modes

| Mode              | Description             |
| ----------------- | ----------------------- |
| `MODE_PERMISSIVE` | Accepts non-strict JSON |
| `MODE_RFC4627`    | Standard JSON           |
| `MODE_STRICTEST`  | Strict parsing          |

Example:

```java
JSONParser parser = new JSONParser(JSONParser.MODE_STRICTEST);
```

---

# When to Use json-smart

Good for:

* Lightweight libraries
* Security/token libraries
* Small internal tools
* Performance-sensitive parsing

Less ideal for:

* Complex object mapping
* Large DTO serialization

For those cases, **Jackson** or **Gson** are usually better.

---

# Common Pitfall

Numbers are returned as `Long` or `Double`, so casting incorrectly can break code:

❌

```java
Integer age = (Integer) obj.get("age");
```

✅

```java
Long age = (Long) obj.get("age");
```

---

# Example: Real-World Use Case

Many security libraries (like **Nimbus JOSE + JWT**) use `json-smart` internally to parse **JWT payloads**, because it is:

* fast
* small
* dependency-friendly