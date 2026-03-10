`org.springframework.cloud:spring-cloud-starter-config` is a Spring Cloud starter dependency that enables your Spring Boot application to **fetch configuration from a centralized Spring Cloud Config Server**. Unlike `spring-cloud-starter-bootstrap`, this starter is focused specifically on **Config Client functionality** for managing externalized properties across environments.

Here’s a concise guide:

---

## 1. Purpose

* **Centralized configuration management:** Fetch properties from a remote Config Server instead of hardcoding them locally.
* **Profile-specific configuration:** Supports different environments (e.g., `dev`, `prod`) with different property sets.
* **Dynamic property updates:** Can work with `@RefreshScope` to refresh beans when configuration changes.

---

## 2. Maven/Gradle Setup

**Maven:**

```xml id="qvn8z7"
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

**Gradle:**

```gradle id="p9z5xv"
implementation 'org.springframework.cloud:spring-cloud-starter-config'
```

> ⚠️ Ensure Spring Cloud version matches your Spring Boot version (e.g., Spring Boot 3.x → Spring Cloud 2022.x).

---

## 3. Configuring the Client

Add properties in `application.yml` (or `bootstrap.yml` if you want early loading):

```yaml id="ykx1uq"
spring:
  application:
    name: my-service
  cloud:
    config:
      uri: https://config-server.example.com
      fail-fast: true
      profile: dev
```

Explanation:

* `spring.application.name` → identifies which config properties to fetch from the server.
* `spring.cloud.config.uri` → URL of the Spring Cloud Config Server.
* `spring.cloud.config.profile` → the environment profile (e.g., `dev`, `prod`).
* `fail-fast` → if `true`, the application fails to start if the Config Server is unreachable.

---

## 4. Accessing Remote Properties

Remote properties can be accessed like local ones:

```yaml id="8gk0iv"
# config-server repo (my-service-dev.yml)
greeting.message: "Hello from Config Server!"
```

```java id="s3t2nb"
@RestController
public class GreetingController {

    @Value("${greeting.message}")
    private String message;

    @GetMapping("/greet")
    public String greet() {
        return message;
    }
}
```

When the application starts, `greeting.message` is fetched from the Config Server instead of `application.yml`.

---

## 5. Refreshing Properties at Runtime

Use `@RefreshScope` to allow beans to reload configuration without restarting:

```java id="v9x3dt"
@RefreshScope
@RestController
public class GreetingController {

    @Value("${greeting.message}")
    private String message;

    @GetMapping("/greet")
    public String greet() {
        return message;
    }
}
```

* Trigger refresh via Spring Actuator endpoint `/actuator/refresh`.

---

## 6. Typical Use Cases

* Multi-environment microservices needing centralized configs.
* Sensitive configs (e.g., passwords) managed in a secure Config Server.
* Updating configuration without redeploying services.

---

### ⚠️ Notes

* Often used **together** with `spring-cloud-starter-bootstrap` if early loading is required.
* Can integrate with Vault, Kubernetes ConfigMaps, or Git-based Config Server repositories.

---