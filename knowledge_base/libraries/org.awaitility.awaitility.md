**Awaitility** is a small Java library designed for **testing asynchronous code**. It lets you **wait for a condition to become true** instead of using `Thread.sleep()` in tests.

It is commonly used in tests for:

* asynchronous processing
* message queues
* event-driven systems
* microservices
* background tasks

Typical stacks where it's useful: **JUnit + Spring Boot + async services**.

---

# 1. Dependency

### Maven

```xml
<dependency>
    <groupId>org.awaitility</groupId>
    <artifactId>awaitility</artifactId>
    <version>4.2.0</version>
    <scope>test</scope>
</dependency>
```

### Gradle

```gradle
testImplementation 'org.awaitility:awaitility:4.2.0'
```

---

# 2. The Core Idea

Instead of this ❌

```java
Thread.sleep(5000);
assertEquals("DONE", service.getStatus());
```

You write this ✅

```java
await().until(() -> service.getStatus().equals("DONE"));
```

Awaitility will:

1. repeatedly check the condition
2. stop when it becomes true
3. fail if the timeout is reached

---

# 3. Basic Usage

```java
import static org.awaitility.Awaitility.await;

await()
    .until(() -> service.isCompleted());
```

Default behavior:

* timeout: **10 seconds**
* poll interval: **100 ms**

---

# 4. Setting Timeout

```java
await()
    .atMost(5, TimeUnit.SECONDS)
    .until(() -> service.isCompleted());
```

Meaning:

> wait up to **5 seconds** until the condition becomes true.

---

# 5. Waiting for a Value

Example: wait until a database value changes.

```java
await()
    .until(() -> repository.count() == 5);
```

---

# 6. Using Assertions

You can combine Awaitility with assertions:

```java
await()
    .atMost(5, TimeUnit.SECONDS)
    .untilAsserted(() ->
        assertEquals(5, repository.count())
    );
```

This is very common in **JUnit tests**.

---

# 7. Poll Interval

Control how often the condition is checked.

```java
await()
    .pollInterval(200, TimeUnit.MILLISECONDS)
    .atMost(5, TimeUnit.SECONDS)
    .until(() -> service.isCompleted());
```

---

# 8. Ignoring Exceptions

Useful if the condition may temporarily throw exceptions.

```java
await()
    .ignoreExceptions()
    .until(() -> repository.findById(id).isPresent());
```

Example scenario:

* record not yet created
* query throws exception
* retry until it exists

---

# 9. Example: Testing Async Service

```java
@Test
void shouldProcessOrderAsync() {

    orderService.createOrder("123");

    await()
        .atMost(10, TimeUnit.SECONDS)
        .until(() -> orderRepository.findById("123")
            .map(Order::isProcessed)
            .orElse(false));
}
```

Flow:

1. create order
2. background worker processes it
3. Awaitility waits until it becomes processed

---

# 10. Best Practices

✔ Prefer **`untilAsserted()`** with JUnit assertions
✔ Keep timeouts **small** (2–10 seconds)
✔ Avoid `Thread.sleep()` in tests
✔ Use Awaitility for **eventual consistency**

Example best practice:

```java
await()
    .atMost(Duration.ofSeconds(5))
    .untilAsserted(() ->
        assertThat(repository.count()).isEqualTo(3)
    );
```

---

# 11. Typical Use Cases

Awaitility is commonly used for testing:

* **Spring @Async methods**
* **Kafka consumers**
* **RabbitMQ listeners**
* **event-driven microservices**
* **eventual consistency**
* **background jobs**

---

✅ **Summary**

**Awaitility** provides a **clean way to test asynchronous behavior** by polling conditions until they succeed instead of relying on fixed sleeps.

Key method:

```java
await().until(condition);
```