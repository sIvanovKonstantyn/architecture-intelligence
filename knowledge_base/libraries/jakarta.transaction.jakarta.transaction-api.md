## What is `jakarta.transaction:jakarta.transaction-api`

`jakarta.transaction:jakarta.transaction-api` is the **Jakarta Transactions specification (JTA)**.
It defines **standard APIs for managing transactions in Java applications**, especially when multiple resources (databases, messaging systems, etc.) must participate in a single atomic operation.

Key idea:

> A **transaction** ensures that a group of operations either **all succeed or all fail**.

Example scenario:

```
1. Save order
2. Update inventory
3. Charge payment
```

If step 3 fails, steps 1 and 2 must be **rolled back**.

The Jakarta Transactions API defines interfaces such as:

* `UserTransaction`
* `TransactionManager`
* `Transaction`
* `Synchronization`

But just like with the persistence API, **this dependency only provides the specification**, not the implementation.

Typical implementations:

* Narayana
* Atomikos
* Bitronix Transaction Manager

Frameworks like Spring Boot typically abstract most of this behind `@Transactional`.

---

# Quick Guide: Using Jakarta Transaction API

## 1. Add Dependency

Maven:

```xml
<dependency>
    <groupId>jakarta.transaction</groupId>
    <artifactId>jakarta.transaction-api</artifactId>
    <version>2.0.1</version>
</dependency>
```

Again, this only provides **interfaces**.

A runtime environment (application server or framework) must provide the **transaction manager implementation**.

---

# 2. Declarative Transactions (Most Common)

The easiest way to use Jakarta transactions is with the `@Transactional` annotation.

```java
import jakarta.transaction.Transactional;

@Transactional
public void createOrder(Order order) {

    orderRepository.save(order);
    inventoryService.reserve(order.getItems());
    paymentService.charge(order);

}
```

Behavior:

```
Start transaction
    ↓
Execute method
    ↓
If success → COMMIT
If exception → ROLLBACK
```

Rollback occurs automatically on runtime exceptions.

---

# 3. Using `UserTransaction` (Programmatic)

In environments like Jakarta EE application servers you can manually control transactions.

```java
import jakarta.transaction.UserTransaction;

@Inject
UserTransaction tx;

public void transferMoney() throws Exception {

    tx.begin();

    try {
        accountDao.withdraw(100);
        accountDao.deposit(100);

        tx.commit();
    } catch (Exception e) {
        tx.rollback();
    }
}
```

Lifecycle:

```
begin()
execute business logic
commit() OR rollback()
```

---

# 4. Transaction Propagation

`@Transactional` supports propagation rules.

Example:

```java
@Transactional(Transactional.TxType.REQUIRED)
public void processPayment() {
}
```

Common types:

| Type            | Behavior                                |
| --------------- | --------------------------------------- |
| `REQUIRED`      | Join existing transaction or create new |
| `REQUIRES_NEW`  | Always start a new transaction          |
| `MANDATORY`     | Must run inside transaction             |
| `SUPPORTS`      | Run with or without transaction         |
| `NOT_SUPPORTED` | Suspend existing transaction            |

---

# 5. Transaction Synchronization

You can attach logic before or after a transaction completes.

```java
transaction.registerSynchronization(new Synchronization() {

    public void beforeCompletion() {
        log.info("Before commit");
    }

    public void afterCompletion(int status) {
        log.info("Transaction finished");
    }
});
```

Useful for:

* cache invalidation
* messaging
* auditing

---

# Typical Usage in Modern Applications

In most real-world apps:

```
Jakarta Transactions API
        ↓
Framework (Spring / Jakarta EE)
        ↓
Transaction Manager (Narayana, etc.)
        ↓
Database
```

Developers usually interact only with:

```
@Transactional
```

---

# Example with Persistence

A common combination is:

* `jakarta.persistence-api`
* `jakarta.transaction-api`

Example service:

```java
import jakarta.transaction.Transactional;

@Transactional
public class UserService {

    @PersistenceContext
    EntityManager em;

    public void registerUser(User user) {
        em.persist(user);
    }
}
```

The transaction ensures:

```
persist()
flush()
commit()
```

happen atomically.

---

# Common Pitfall

Developers sometimes include only:

```
jakarta.transaction-api
```

But **without a transaction manager implementation**, the API does nothing.

---

# Quick Summary

| Component                 | Role                            |
| ------------------------- | ------------------------------- |
| `jakarta.transaction-api` | Transaction specification       |
| Transaction Manager       | Implementation                  |
| `@Transactional`          | Declarative transaction control |
| `UserTransaction`         | Manual transaction control      |

---

✅ **Rule of thumb**

```
jakarta.transaction-api → specification
Transaction Manager → implementation
```