`org.springframework.cloud:spring-cloud-starter-bootstrap` is a Spring Cloud starter dependency that helps enable **bootstrap context** features in a Spring Boot application. It’s mainly used to load configuration properties **early in the application lifecycle**, before the main `ApplicationContext` is created, so that those properties can influence things like config server integration, property sources, or dynamic environment setup.

Here’s a short guide:

---

## 1. Purpose

* **Early property loading:** Some properties need to be available before the normal `ApplicationContext` is initialized, e.g., properties for Spring Cloud Config Server (`spring.cloud.config.uri`) or for setting the application name dynamically.
* **Supports `bootstrap.yml` or `bootstrap.properties`:** This file is loaded **before** `application.yml`/`application.properties`.
* **Enables Config Client features:** Works with Spring Cloud Config to fetch remote properties, decryption, or profile-specific configuration early.

---

## 2. Maven/Gradle Setup

**Maven:**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bootstrap</artifactId>
</dependency>
```

**Gradle:**

```gradle
implementation 'org.springframework.cloud:spring-cloud-starter-bootstrap'
```

> ⚠️ Make sure your Spring Cloud version is compatible with your Spring Boot version. For example, Spring Boot 3.x works with Spring Cloud 2022.x.

---

## 3. Adding `bootstrap.yml`

Create a `src/main/resources/bootstrap.yml` file:

```yaml
spring:
  application:
    name: my-service
  cloud:
    config:
      uri: https://config-server.example.com
      fail-fast: true
```

Key points:

* `spring.application.name` — used to locate config properties for this service.
* `spring.cloud.config.uri` — points to your Config Server.
* This file is loaded **before** `application.yml`, so you can use remote properties in your main context.

---

## 4. How It Works

1. Spring Boot starts → initializes **BootstrapContext**.
2. Loads `bootstrap.yml` / `bootstrap.properties`.
3. Fetches remote configurations or decrypts secrets.
4. Creates the main `ApplicationContext` with all the properties available.

---

## 5. Common Use Cases

* Spring Cloud Config integration.
* Centralized configuration with multiple environments.
* Early property resolution for logging, profiles, or secrets.
* Dynamic environment variables before main application startup.

---

## 6. Example

```java
@SpringBootApplication
public class MyServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyServiceApplication.class, args);
    }
}
```

With `bootstrap.yml`, your service can fetch remote configuration even **before beans are created**, allowing other components to rely on those properties immediately.

---

### ⚠️ Notes

* Starting from **Spring Cloud 2022.x**, `bootstrap.yml` is **deprecated by default**, but the starter provides backward compatibility.
* If you don’t need early config loading, you can skip this starter and configure everything in `application.yml`.