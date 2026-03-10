## ☕ Short Guide: Using Caffeine Cache in Java

**Caffeine** (`com.github.ben-manes.caffeine:caffeine`) is a **high-performance Java caching library** that serves as a modern replacement for Guava Cache. It provides near-optimal caching with advanced eviction policies and excellent concurrency performance.

It is commonly used in **Spring Boot applications, microservices, and high-throughput systems** to cache frequently accessed data and reduce load on databases or external APIs.

---

# 1️⃣ Add Dependency

### Maven

```xml
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
    <version>3.1.8</version>
</dependency>
```

### Gradle

```gradle
implementation 'com.github.ben-manes.caffeine:caffeine:3.1.8'
```

---

# 2️⃣ Basic Cache Example

```java
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;

import java.util.concurrent.TimeUnit;

Cache<String, String> cache = Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .build();

cache.put("key", "value");

String value = cache.getIfPresent("key");
```

---

# 3️⃣ Loading Cache (Automatic Loading)

A **LoadingCache** automatically loads values when they are missing.

```java
import com.github.benmanes.caffeine.cache.LoadingCache;

LoadingCache<String, String> cache =
        Caffeine.newBuilder()
                .maximumSize(1000)
                .expireAfterWrite(5, TimeUnit.MINUTES)
                .build(key -> loadData(key));

String value = cache.get("user:123");
```

Example loader:

```java
private String loadData(String key) {
    System.out.println("Loading data for " + key);
    return "data";
}
```

📌 If the key is missing, the loader function is called automatically.

---

# 4️⃣ Asynchronous Cache

Useful when loading data requires **remote calls or database queries**.

```java
import com.github.benmanes.caffeine.cache.AsyncLoadingCache;

AsyncLoadingCache<String, String> cache =
        Caffeine.newBuilder()
                .maximumSize(1000)
                .buildAsync(key -> loadAsync(key));

CompletableFuture<String> future = cache.get("key");
```

---

# 5️⃣ Common Eviction Policies

### Maximum Size

```java
.maximumSize(10_000)
```

Evicts least-recently used entries when limit is reached.

---

### Expire After Write

```java
.expireAfterWrite(10, TimeUnit.MINUTES)
```

Entry expires after a fixed time since creation.

---

### Expire After Access

```java
.expireAfterAccess(5, TimeUnit.MINUTES)
```

Entry expires if not accessed for a period.

---

### Refresh After Write

```java
.refreshAfterWrite(5, TimeUnit.MINUTES)
```

Entry is refreshed asynchronously after the specified time.

---

# 6️⃣ Cache Statistics

Enable metrics for monitoring:

```java
Cache<String, String> cache = Caffeine.newBuilder()
        .maximumSize(1000)
        .recordStats()
        .build();
```

Retrieve statistics:

```java
System.out.println(cache.stats());
```

Example output:

```
CacheStats{hitCount=1200, missCount=300, loadSuccessCount=300}
```

---

# 7️⃣ Removal Listener

Useful for logging or cleanup when entries are evicted.

```java
Cache<String, String> cache =
        Caffeine.newBuilder()
                .maximumSize(100)
                .removalListener((key, value, cause) ->
                        System.out.println("Removed " + key + " because " + cause))
                .build();
```

---

# 8️⃣ Spring Boot Integration

Spring Boot supports Caffeine via **Spring Cache abstraction**.

### Dependency

```xml
<dependency>
 <groupId>org.springframework.boot</groupId>
 <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

### Enable caching

```java
@EnableCaching
@SpringBootApplication
public class App {}
```

### Configure Caffeine

```java
@Bean
public CacheManager cacheManager() {
    CaffeineCacheManager manager = new CaffeineCacheManager();
    manager.setCaffeine(Caffeine.newBuilder()
        .maximumSize(1000)
        .expireAfterWrite(10, TimeUnit.MINUTES));
    return manager;
}
```

### Use cache

```java
@Cacheable("users")
public User getUser(String id) {
    return userRepository.findById(id);
}
```

---

# 9️⃣ When to Use Caffeine

Good for:

✔ API response caching
✔ database query caching
✔ configuration lookups
✔ rate-limiting counters
✔ expensive computations

---

# 🔟 Why Caffeine Is Popular

Compared to older libraries:

| Feature               | Caffeine |
| --------------------- | -------- |
| High throughput       | ✅        |
| Lock-free algorithms  | ✅        |
| Async loading         | ✅        |
| Near-optimal eviction | ✅        |
| Spring Boot support   | ✅        |

Caffeine uses advanced algorithms like **Window TinyLFU**, which provides better cache hit rates than traditional LRU caches.

---

💡 **Typical real-world example in your Spring Boot crypto services:**

Cache things like:

* symbol metadata
* market info
* TradingView indicators
* expensive strategy calculations

instead of requesting them repeatedly.