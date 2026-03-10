`org.springframework.boot:spring-boot-starter-data-redis` is the **Spring Boot starter for Redis**. It provides auto-configuration, dependencies, and utilities to work with Redis in a Spring Boot application. Redis can be used for caching, messaging (via Pub/Sub), or storing key-value data.

Here’s a **short guide** to using it:

---

## 1. Add the dependency

If you use **Maven**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

For **Gradle**:

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
```

---

## 2. Configure Redis connection

Spring Boot auto-configures Redis if you provide connection details in `application.properties` or `application.yml`.

**Example (`application.properties`):**

```properties
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password=yourpassword  # optional
spring.redis.timeout=2000
```

**Example (`application.yml`):**

```yaml
spring:
  redis:
    host: localhost
    port: 6379
    password: yourpassword
    timeout: 2000
```

---

## 3. Use `RedisTemplate` for Redis operations

Spring Boot provides `RedisTemplate` for working with keys, values, hashes, lists, sets, and sorted sets.

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

@Service
public class RedisExampleService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public void saveValue(String key, Object value) {
        redisTemplate.opsForValue().set(key, value);
    }

    public Object getValue(String key) {
        return redisTemplate.opsForValue().get(key);
    }
}
```

> `opsForValue()` is for simple key-value pairs. Other operations exist:
>
> * `opsForHash()` – for Redis hashes
> * `opsForList()` – for lists
> * `opsForSet()` – for sets
> * `opsForZSet()` – for sorted sets

---

## 4. Enable caching with Redis

If you want to use Redis as a **cache**, add `@EnableCaching` in a configuration class:

```java
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
public class CacheConfig {
}
```

Then you can use `@Cacheable`:

```java
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class ProductService {

    @Cacheable(value = "products", key = "#id")
    public Product getProductById(Long id) {
        // expensive DB call
        return fetchFromDatabase(id);
    }
}
```

Spring Boot automatically stores `products` in Redis.

---

## 5. Optional: Use Lettuce or Jedis

* Spring Boot uses **Lettuce** as default Redis client (reactive and thread-safe).
* You can switch to **Jedis** by adding:

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

---

✅ **Summary:** `spring-boot-starter-data-redis` makes it easy to connect Spring Boot apps to Redis for caching, messaging, and key-value storage with minimal configuration.

---