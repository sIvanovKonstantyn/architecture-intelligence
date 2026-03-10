`org.keycloak.keycloak-core` is a **Java library module** from **Keycloak**, the open-source identity and access management solution. This module contains **core classes and utilities** for working with Keycloak internally or embedding Keycloak functionality in Java applications, such as realm models, users, roles, and events. It doesn’t include server APIs or REST endpoints — those are in other modules like `keycloak-server-spi` or `keycloak-services`.

Here’s a short guide on its usage:

---

## 1. **Maven Dependency**

To use `keycloak-core`, include it in your Maven project:

```xml
<dependency>
    <groupId>org.keycloak</groupId>
    <artifactId>keycloak-core</artifactId>
    <version>21.1.1</version> <!-- or your desired version -->
</dependency>
```

For Gradle:

```gradle
implementation "org.keycloak:keycloak-core:21.1.1"
```

> **Note:** Replace the version with the one compatible with your Keycloak server or libraries.

---

## 2. **Common Uses**

### a) **Working with Keycloak Models**

You can interact with in-memory representations of realms, users, roles, and clients.

```java
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.RealmModel;
import org.keycloak.models.UserModel;

public void printUsers(KeycloakSession session, String realmName) {
    RealmModel realm = session.realms().getRealmByName(realmName);
    for (UserModel user : session.users().getUsers(realm)) {
        System.out.println(user.getUsername());
    }
}
```

* `KeycloakSession` provides access to all Keycloak services in a transaction.
* `RealmModel` and `UserModel` are core abstractions for realms and users.

---

### b) **Working with Events**

You can handle events (like login or registration) using Keycloak’s internal `EventBuilder`:

```java
import org.keycloak.events.EventBuilder;
import org.keycloak.models.KeycloakSession;

public void logLoginEvent(KeycloakSession session, String realmName, String userId) {
    EventBuilder event = new EventBuilder(session.getContext().getRealm(), session, session.getContext().getConnection());
    event.event(org.keycloak.events.EventType.LOGIN)
         .user(userId)
         .detail("info", "User logged in")
         .success();
}
```

---

### c) **Utility Classes**

`keycloak-core` also provides helper utilities:

* `org.keycloak.common.util.Time` – for time-related operations.
* `org.keycloak.common.util.SecretGenerator` – to generate secure secrets.
* `org.keycloak.common.util.Base64Url` – for encoding data safely.

Example:

```java
import org.keycloak.common.util.SecretGenerator;

String secret = SecretGenerator.getInstance().randomString(32);
System.out.println("Generated secret: " + secret);
```

---

## 3. **Key Notes**

* **Not a full server module:** To expose REST APIs, you need `keycloak-server-spi` or `keycloak-services`.
* **Embedded usage:** Often used when writing Keycloak extensions, custom providers, or testing Keycloak logic without running a full server.
* **Session management:** All model operations require a `KeycloakSession`, which is typically injected in providers.