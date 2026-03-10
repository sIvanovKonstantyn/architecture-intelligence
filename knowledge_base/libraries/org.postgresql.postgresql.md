`org.postgresql:postgresql` is the official **PostgreSQL JDBC driver** for Java. It allows Java applications to connect to a PostgreSQL database and execute SQL queries. Here’s a concise guide on how to use it.

---

## 1. **Add Dependency**

### Maven

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version> <!-- check for latest version -->
</dependency>
```

### Gradle

```gradle
implementation 'org.postgresql:postgresql:42.6.0'
```

---

## 2. **Basic Usage**

### Connect to PostgreSQL

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgresExample {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/mydb";
        String user = "postgres";
        String password = "secret";

        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            System.out.println("Connected to PostgreSQL successfully!");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

* `jdbc:postgresql://host:port/database` is the JDBC URL format.
* The driver class `org.postgresql.Driver` is automatically loaded by `DriverManager` in modern versions.

---

### Execute a Query

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class QueryExample {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:postgresql://localhost:5432/mydb";
        String user = "postgres";
        String password = "secret";

        try (Connection conn = DriverManager.getConnection(url, user, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT id, name FROM users")) {

            while (rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                System.out.println(id + ": " + name);
            }
        }
    }
}
```

---

### Notes & Tips

* **Transactions**: Auto-commit is true by default. For transactions, use `conn.setAutoCommit(false)` and `conn.commit()`/`conn.rollback()`.
* **Connection Pooling**: For production, use a pool like HikariCP instead of creating raw connections.
* **SSL**: Add `?sslmode=require` to JDBC URL if your database requires SSL.
* **Large Objects**: The driver supports PostgreSQL-specific features like arrays, JSON, UUIDs, and `LargeObject` streaming.

---

This driver is widely used in Spring Boot, plain JDBC applications, and frameworks like Hibernate for PostgreSQL support.