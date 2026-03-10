**Flyway** is a **database migration tool** used to **version, manage, and automate database schema changes**.
The artifact **`org.flywaydb:flyway-core`** is the core Java library that provides Flyway functionality for managing migrations in Java applications.

It is widely used with frameworks like **Spring Boot**, **Hibernate**, and plain Java applications to keep database schema changes synchronized with application code.

---

# Flyway Quick Guide

## 1. Why Flyway?

Flyway solves several common problems:

* Versioning database schema changes
* Automating database updates during deployment
* Keeping multiple environments consistent (dev, test, prod)
* Avoiding manual SQL execution
* Tracking which migrations were applied

Flyway maintains a **schema history table** (`flyway_schema_history`) in the database to track executed migrations.

---

# 2. Adding Flyway Dependency

### Maven

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
    <version>10.0.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.flywaydb:flyway-core:10.0.0'
```

---

# 3. Migration File Naming Convention

Flyway automatically detects migration files with this format:

```
V<version>__<description>.sql
```

Example:

```
V1__create_user_table.sql
V2__add_email_column.sql
V3__create_orders_table.sql
```

Typical location:

```
src/main/resources/db/migration
```

---

# 4. Example Migration

### `V1__create_users_table.sql`

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200)
);
```

### `V2__add_index.sql`

```sql
CREATE INDEX idx_users_email
ON users(email);
```

---

# 5. Running Flyway in Java

Basic Java example:

```java
import org.flywaydb.core.Flyway;

public class FlywayExample {

    public static void main(String[] args) {

        Flyway flyway = Flyway.configure()
                .dataSource(
                        "jdbc:postgresql://localhost:5432/appdb",
                        "user",
                        "password")
                .load();

        flyway.migrate();
    }
}
```

What happens when `migrate()` runs:

1. Flyway checks `flyway_schema_history`
2. Finds unapplied migrations
3. Executes them in order
4. Records results in the history table

---

# 6. Important Flyway Commands

### Migrate

Apply new migrations

```java
flyway.migrate();
```

---

### Clean ⚠️

Drops all database objects (dangerous in production)

```java
flyway.clean();
```

---

### Validate

Ensures migrations match applied ones

```java
flyway.validate();
```

---

### Repair

Fix migration metadata

```java
flyway.repair();
```

---

### Info

Show migration status

```java
flyway.info();
```

---

# 7. Flyway with Spring Boot

When using **Spring Boot**, Flyway runs automatically.

### Dependency

```xml
<dependency>
 <groupId>org.flywaydb</groupId>
 <artifactId>flyway-core</artifactId>
</dependency>
```

### Configuration

`application.yml`

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
```

At application startup:

1. Flyway runs migrations
2. Database schema is updated automatically

---

# 8. Versioned vs Repeatable Migrations

### Versioned migrations

```
V1__create_table.sql
V2__add_column.sql
```

Executed **once**.

---

### Repeatable migrations

```
R__refresh_views.sql
```

Executed **whenever file checksum changes**.

Useful for:

* Views
* Stored procedures
* Functions

---

# 9. Best Practices

✅ Keep migrations **small and atomic**
✅ Never modify already applied migrations
✅ Always test migrations in staging
✅ Use **repeatable migrations for views/functions**
✅ Use Flyway in **CI/CD pipelines**

---

# 10. Typical Project Structure

```
project
 ├── src
 │   ├── main
 │   │   ├── java
 │   │   └── resources
 │   │        └── db
 │   │            └── migration
 │   │                ├── V1__init.sql
 │   │                ├── V2__add_index.sql
 │   │                └── R__views.sql
```

---

💡 **Tip (important for microservices):**
Each microservice should own **its own Flyway migrations and database schema** to avoid cross-service coupling.