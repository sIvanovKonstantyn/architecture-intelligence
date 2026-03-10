## What is `jakarta.validation:jakarta.validation-api`

`jakarta.validation:jakarta.validation-api` is the **Jakarta Bean Validation specification**.
It defines a **standard way to validate Java objects using annotations**.

The idea is simple:

> Attach **validation rules directly to fields, parameters, or methods**, and let the framework validate them automatically.

Example:

```java
public class User {

    @NotNull
    private String name;

    @Email
    private String email;

    @Min(18)
    private int age;

}
```

This API defines:

* validation annotations (`@NotNull`, `@Size`, `@Email`, etc.)
* validation engine interfaces (`Validator`, `ConstraintValidator`)
* metadata model
* integration hooks for frameworks

However, **the API is only the specification**, not the implementation.

The most widely used implementation is:

* Hibernate Validator

Frameworks like Spring Boot automatically configure it.

---

# Quick Guide: Using Jakarta Validation API

## 1. Add Dependencies

Maven example:

```xml
<dependencies>

    <!-- Bean Validation API -->
    <dependency>
        <groupId>jakarta.validation</groupId>
        <artifactId>jakarta.validation-api</artifactId>
        <version>3.0.2</version>
    </dependency>

    <!-- Implementation -->
    <dependency>
        <groupId>org.hibernate.validator</groupId>
        <artifactId>hibernate-validator</artifactId>
        <version>8.0.1.Final</version>
    </dependency>

</dependencies>
```

---

# 2. Add Validation Annotations

Example DTO:

```java
import jakarta.validation.constraints.*;

public class UserRequest {

    @NotBlank
    @Size(min = 2, max = 50)
    private String name;

    @Email
    @NotNull
    private String email;

    @Min(18)
    @Max(120)
    private int age;

}
```

Common annotations:

| Annotation      | Meaning                        |
| --------------- | ------------------------------ |
| `@NotNull`      | value must not be null         |
| `@NotBlank`     | string must contain characters |
| `@Size`         | length constraints             |
| `@Min` / `@Max` | numeric limits                 |
| `@Email`        | valid email format             |
| `@Pattern`      | regex validation               |

---

# 3. Validate an Object Programmatically

Example using `Validator`.

```java
import jakarta.validation.*;

ValidatorFactory factory =
        Validation.buildDefaultValidatorFactory();

Validator validator = factory.getValidator();

UserRequest request = new UserRequest();
request.setEmail("wrong-email");

Set<ConstraintViolation<UserRequest>> violations =
        validator.validate(request);

for (ConstraintViolation<UserRequest> v : violations) {
    System.out.println(v.getPropertyPath() + " " + v.getMessage());
}
```

Example output:

```
email must be a well-formed email address
name must not be blank
```

---

# 4. Method Parameter Validation

Validation can also apply to method parameters.

```java
public class UserService {

    public void register(
        @NotBlank String name,
        @Email String email
    ) {
        // business logic
    }

}
```

---

# 5. Validation Groups

Groups allow different validation rules depending on context.

Example:

```java
public interface Create {}
public interface Update {}
```

DTO:

```java
public class UserDTO {

    @Null(groups = Create.class)
    @NotNull(groups = Update.class)
    private Long id;

}
```

Usage:

```java
validator.validate(user, Create.class);
```

---

# 6. Custom Validator

You can create your own annotation.

### Step 1 — annotation

```java
@Target({FIELD})
@Retention(RUNTIME)
@Constraint(validatedBy = UsernameValidator.class)
public @interface ValidUsername {

    String message() default "Invalid username";

    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

---

### Step 2 — validator

```java
public class UsernameValidator
        implements ConstraintValidator<ValidUsername, String> {

    public boolean isValid(String value,
                           ConstraintValidatorContext ctx) {

        return value != null && value.matches("[a-zA-Z0-9_]+");
    }

}
```

Usage:

```java
@ValidUsername
private String username;
```

---

# 7. Validation with REST APIs

In web frameworks like Spring Boot validation is automatic.

Example controller:

```java
@PostMapping("/users")
public ResponseEntity createUser(
        @Valid @RequestBody UserRequest request) {

    return ResponseEntity.ok().build();
}
```

If validation fails:

```
HTTP 400 Bad Request
```

---

# Typical Validation Flow

```
Client Request
      ↓
DTO with validation annotations
      ↓
Validation engine
      ↓
If valid → service logic
If invalid → validation error response
```

---

# Advantages

* Declarative validation via annotations
* Centralized rules
* Works with DTOs, entities, APIs
* Standard across frameworks
* Easy integration with REST and persistence layers

---

# Common Pitfall

Many developers add only:

```
jakarta.validation-api
```

But the API **does not contain the validation engine**.

You must add an implementation such as:

* Hibernate Validator

---

# Quick Summary

| Component                      | Role                          |
| ------------------------------ | ----------------------------- |
| `jakarta.validation-api`       | Bean Validation specification |
| `Hibernate Validator`          | Implementation                |
| Annotations (`@NotNull`, etc.) | Declare rules                 |
| `Validator`                    | Executes validation           |

---

✅ **Rule of thumb**

```
jakarta.validation-api → specification
hibernate-validator → implementation
```