`io.awspring.cloud:spring-cloud-aws-starter-parameter-store` is a **Spring Boot starter** that allows your application to **load configuration directly from AWS Systems Manager Parameter Store**.

It integrates with Spring Boot’s **ConfigData API**, so parameters stored in AWS become available as **Spring properties** (`@Value`, `@ConfigurationProperties`, etc.).

This is commonly used to **externalize configuration and secrets** in AWS environments.

The starter is part of the Spring Cloud AWS ecosystem and works with Spring Boot.

---

# Quick Guide: Using Spring Cloud AWS Parameter Store

## 1. Add dependency

Maven:

```xml
<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-parameter-store</artifactId>
</dependency>
```

Gradle:

```gradle
implementation 'io.awspring.cloud:spring-cloud-aws-starter-parameter-store'
```

---

# 2. Create parameters in AWS

Open **Parameter Store** in
AWS Systems Manager.

Example parameters:

```
/config/my-service/db.url
/config/my-service/db.username
/config/my-service/db.password
```

Types supported:

* String
* StringList
* SecureString (recommended for secrets)

Example:

```
Name: /config/my-service/api.key
Type: SecureString
Value: secret-key
```

---

# 3. Configure Spring Boot to load parameters

Add to `application.yml`:

```yaml
spring:
  config:
    import: aws-parameterstore:/config/my-service/
```

This tells Spring Boot:

> Load all parameters under `/config/my-service/`.

Spring will automatically map them to properties.

Example mapping:

```
/config/my-service/db.url
```

becomes

```
db.url
```

---

# 4. Use properties in your application

### Using `@Value`

```java
@Value("${db.url}")
private String dbUrl;
```

---

### Using `@ConfigurationProperties`

```java
@ConfigurationProperties(prefix = "db")
public class DatabaseConfig {

    private String url;
    private String username;
    private String password;

}
```

---

# 5. Configure AWS credentials

The starter uses the default AWS credential chain from the
Amazon Web Services SDK.

Supported sources:

* EC2 instance role
* ECS / EKS role
* environment variables

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

* AWS CLI profile

```
~/.aws/credentials
```

---

# 6. Working with SecureString parameters

If a parameter is stored as `SecureString`, it will be **automatically decrypted**.

Example:

```
/config/my-service/db.password
```

Used the same way in Spring:

```java
@Value("${db.password}")
private String password;
```

---

# 7. Optional: Use hierarchical configs

Example structure:

```
/config/my-service/dev/db.url
/config/my-service/prod/db.url
```

Then import based on profile:

```yaml
spring:
  config:
    import: aws-parameterstore:/config/my-service/${spring.profiles.active}/
```

---

# Example Result

AWS parameters:

```
/config/my-service/db.url=jdbc:postgresql://db:5432/app
/config/my-service/db.username=app
/config/my-service/db.password=secret
```

Spring can use:

```
db.url
db.username
db.password
```

---

# Why Use Parameter Store

Advantages:

* centralized config
* secret management
* environment separation
* no secrets in Git
* native Spring integration

Common production usage:

```
AWS Parameter Store
        ↓
Spring Cloud AWS
        ↓
Spring Boot Config
        ↓
@ConfigurationProperties
```

---

💡 **Typical use case**

A Spring Boot service deployed on AWS (ECS/EKS/EC2) loads configuration like:

* DB credentials
* API keys
* feature flags
* service endpoints

from **Parameter Store at startup**.