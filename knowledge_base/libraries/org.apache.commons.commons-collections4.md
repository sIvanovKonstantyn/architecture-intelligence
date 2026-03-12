**`org.apache.commons:commons-collections4`** is a Java library from the Apache Software Foundation that extends the Java Collections Framework with additional data structures, utilities, and functional-style helpers.

It provides advanced collection implementations and utilities that are missing in standard `java.util` collections.

---

# Quick Guide: Apache Commons Collections 4

## 1. Dependency

### Maven

```xml
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-collections4</artifactId>
  <version>4.5.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.apache.commons:commons-collections4:4.5.0'
```

---

# Core Features

## 1. Collection Utilities

The `CollectionUtils` class provides helper methods for working with collections.

### Example: null-safe operations

```java
import org.apache.commons.collections4.CollectionUtils;

List<String> a = List.of("A", "B", "C");
List<String> b = List.of("B", "C", "D");

Collection<String> intersection = CollectionUtils.intersection(a, b);
System.out.println(intersection); // [B, C]
```

Useful methods:

```
CollectionUtils.isEmpty(collection)
CollectionUtils.isNotEmpty(collection)
CollectionUtils.intersection(a, b)
CollectionUtils.subtract(a, b)
CollectionUtils.union(a, b)
CollectionUtils.containsAny(a, b)
```

---

# 2. Iterable Utilities

`IterableUtils` adds functional-style helpers.

```java
import org.apache.commons.collections4.IterableUtils;

Iterable<String> filtered =
    IterableUtils.filteredIterable(list, s -> s.startsWith("A"));
```

---

# 3. Map Utilities

`MapUtils` simplifies safe map access.

```java
import org.apache.commons.collections4.MapUtils;

Map<String, Integer> map = Map.of("a", 1);

int value = MapUtils.getIntValue(map, "b", 0);
```

Key benefits:

* default values
* null-safe access
* type conversions

Common methods:

```
MapUtils.getString(map, key)
MapUtils.getIntValue(map, key, default)
MapUtils.isEmpty(map)
```

---

# 4. Advanced Collection Types

Commons Collections includes specialized collections not in standard Java.

### MultiValuedMap (map → multiple values)

```java
import org.apache.commons.collections4.MultiValuedMap;
import org.apache.commons.collections4.multimap.ArrayListValuedHashMap;

MultiValuedMap<String, String> map = new ArrayListValuedHashMap<>();

map.put("fruit", "apple");
map.put("fruit", "banana");

System.out.println(map.get("fruit")); 
// [apple, banana]
```

---

### BidiMap (two-way map)

```java
import org.apache.commons.collections4.BidiMap;
import org.apache.commons.collections4.bidimap.DualHashBidiMap;

BidiMap<Integer, String> map = new DualHashBidiMap<>();

map.put(1, "one");

String value = map.get(1);
Integer key = map.getKey("one");
```

Useful when you need fast reverse lookups.

---

### Bag (multiset)

`Bag` counts occurrences of elements.

```java
import org.apache.commons.collections4.Bag;
import org.apache.commons.collections4.bag.HashBag;

Bag<String> bag = new HashBag<>();

bag.add("apple");
bag.add("apple");
bag.add("banana");

System.out.println(bag.getCount("apple")); // 2
```

---

# 5. Collection Decorators

Commons Collections provides wrappers that add behavior to collections.

### Predicated Collection

Automatically validates elements.

```java
import org.apache.commons.collections4.collection.PredicatedCollection;

Collection<String> safeCollection =
    PredicatedCollection.predicatedCollection(
        new ArrayList<>(),
        s -> s.length() < 5
    );

safeCollection.add("abc");   // ok
safeCollection.add("abcdef"); // throws IllegalArgumentException
```

---

# 6. Transforming Collections

You can automatically transform elements on insert.

```java
import org.apache.commons.collections4.collection.TransformedCollection;

Collection<String> upper =
    TransformedCollection.transformingCollection(
        new ArrayList<>(),
        String::toUpperCase
    );

upper.add("hello");

System.out.println(upper); // [HELLO]
```

---

# When to Use Commons Collections

Use it when you need:

* `MultiMap` / `MultiValuedMap`
* `Bidirectional maps`
* `Multisets`
* advanced collection utilities
* collection decorators (validation, transformation)

---

# When NOT to Use It

Modern Java already covers many use cases:

| Feature           | Java alternative     |
| ----------------- | -------------------- |
| Filtering         | Streams              |
| Transformations   | Streams              |
| Optional defaults | `Map.getOrDefault()` |

But Commons Collections is still useful for:

* `MultiValuedMap`
* `Bag`
* `BidiMap`
* advanced collection utilities.

---

💡 **Tip for modern Java (Java 17+)**

Combine it with streams:

```java
Collection<String> result =
    CollectionUtils.intersection(list1, list2)
        .stream()
        .map(String::toUpperCase)
        .toList();
```