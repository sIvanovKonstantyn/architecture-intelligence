## What is `jakarta.persistence:jakarta.persistence-api`

`jakarta.persistence:jakarta.persistence-api` is the **official API specification for the Jakarta Persistence framework (formerly JPA)**.
It defines **standard interfaces, annotations, and contracts** for working with relational databases using **ORM (Object-Relational Mapping)** in Java.

Important points:

* It is **only the specification**, not the implementation.
* It defines things like:

  * `@Entity`
  * `@Id`
  * `@OneToMany`
  * `EntityManager`
  * `Query`
  * `Criteria API`
* To actually use it, you need a **JPA implementation**.

Common implementations:

* Hibernate ORM
* EclipseLink
* Apache OpenJPA

In modern Java projects (especially Spring Boot), **Hibernate** is typically used under the hood.

---

# Quick Guide: Using Jakarta Persistence API

## 1. Add Dependencies

You need **two things**:

1. The API
2. An implementation

Example with Maven:

```xml
<dependencies>
    <!-- Jakarta Persistence API -->
    <dependency>
        <groupId>jakarta.persistence</groupId>
        <artifactId>jakarta.persistence-api</artifactId>
        <version>3.1.0</version>
    </dependency>

    <!-- Implementation (Hibernate) -->
    <dependency>
        <groupId>org.hibernate.orm</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>6.4.4.Final</version>
    </dependency>
</dependencies>
```

---

# 2. Define an Entity

Entities represent database tables.

```java
import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    private String email;

    // getters and setters
}
```

Key annotations:

| Annotation        | Purpose                        |
| ----------------- | ------------------------------ |
| `@Entity`         | Marks class as database entity |
| `@Table`          | Defines table name             |
| `@Id`             | Primary key                    |
| `@GeneratedValue` | Auto ID generation             |
| `@Column`         | Column configuration           |

---

# 3. Configure Persistence

In pure Jakarta projects you define `persistence.xml`.

```
src/main/resources/META-INF/persistence.xml
```

Example:

```xml
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             version="3.0">

    <persistence-unit name="example-unit">

        <class>com.example.User</class>

        <properties>
            <property name="jakarta.persistence.jdbc.url"
                      value="jdbc:postgresql://localhost:5432/test"/>
            <property name="jakarta.persistence.jdbc.user"
                      value="postgres"/>
            <property name="jakarta.persistence.jdbc.password"
                      value="password"/>

            <property name="hibernate.hbm2ddl.auto" value="update"/>
        </properties>

    </persistence-unit>

</persistence>
```

---

# 4. Create an EntityManager

`EntityManager` is the **main API entry point**.

```java
import jakarta.persistence.*;

EntityManagerFactory emf =
    Persistence.createEntityManagerFactory("example-unit");

EntityManager em = emf.createEntityManager();
```

---

# 5. Persist an Entity

```java
em.getTransaction().begin();

User user = new User();
user.setName("Alice");
user.setEmail("alice@example.com");

em.persist(user);

em.getTransaction().commit();
```

---

# 6. Query Data

### JPQL query

```java
List<User> users = em.createQuery(
        "SELECT u FROM User u",
        User.class
).getResultList();
```

JPQL operates on **entities, not tables**.

---

### Find by ID

```java
User user = em.find(User.class, 1L);
```

---

# 7. Update Entity

```java
em.getTransaction().begin();

User user = em.find(User.class, 1L);
user.setEmail("new@email.com");

em.getTransaction().commit();
```

Dirty checking automatically updates the row.

---

# 8. Remove Entity

```java
em.getTransaction().begin();

User user = em.find(User.class, 1L);
em.remove(user);

em.getTransaction().commit();
```

---

# Typical Architecture

```
Controller
    ↓
Service
    ↓
Repository / DAO
    ↓
EntityManager
    ↓
Database
```

Frameworks like Spring Boot simplify this using:

* `@Repository`
* `@Transactional`
* Spring Data JPA

---

# Key Advantages

* Standardized ORM API
* Database-agnostic code
* Automatic object ↔ relational mapping
* Query abstraction via JPQL
* Integration with modern frameworks

---

# Common Pitfall

Many developers mistakenly add only:

```
jakarta.persistence-api
```

and expect it to work.

But **without an implementation (like Hibernate)**, the API alone **cannot interact with a database**.

---

✅ **Rule of thumb**

```
jakarta.persistence-api → specification
hibernate-core → implementation
```