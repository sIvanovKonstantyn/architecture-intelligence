`org.springframework.security:spring-security-crypto` is a lightweight Spring Security module that provides **cryptographic utilities** such as password hashing, encoding, and general-purpose encryption helpers. It’s separate from the full Spring Security framework and can be used in any Java project without the full security stack.

Here’s a concise guide:

---

## **1. Add the dependency**

**Maven:**

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-crypto</artifactId>
    <version>6.2.2</version> <!-- use latest version -->
</dependency>
```

**Gradle:**

```gradle
implementation "org.springframework.security:spring-security-crypto:6.2.2"
```

---

## **2. Password hashing with `BCryptPasswordEncoder`**

Spring Security Crypto provides the `PasswordEncoder` interface. The most common implementation is `BCryptPasswordEncoder`:

```java
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

public class PasswordExample {
    public static void main(String[] args) {
        PasswordEncoder encoder = new BCryptPasswordEncoder();

        String rawPassword = "mySecretPassword";
        String hashedPassword = encoder.encode(rawPassword);

        System.out.println("Hashed password: " + hashedPassword);

        // Verify password
        boolean matches = encoder.matches(rawPassword, hashedPassword);
        System.out.println("Password matches: " + matches);
    }
}
```

**Notes:**

* BCrypt automatically generates a salt for each password.
* Use `matches()` to verify passwords instead of comparing strings manually.

---

## **3. Other encoders**

`spring-security-crypto` also provides:

* `Pbkdf2PasswordEncoder` – strong PBKDF2 hashing.
* `SCryptPasswordEncoder` – memory-hard hashing, good against GPU attacks.
* `Argon2PasswordEncoder` – modern password hashing recommended for new projects.

Example:

```java
PasswordEncoder encoder = new Pbkdf2PasswordEncoder();
String hash = encoder.encode("password123");
```

---

## **4. Simple encryption/decryption**

For generic text encryption:

```java
import org.springframework.security.crypto.encrypt.Encryptors;
import org.springframework.security.crypto.encrypt.TextEncryptor;

public class CryptoExample {
    public static void main(String[] args) {
        String password = "secretKey"; // used to generate key
        String salt = "12345678";      // must be 8 chars

        TextEncryptor encryptor = Encryptors.text(password, salt);
        String plaintext = "Hello World!";
        String encrypted = encryptor.encrypt(plaintext);
        String decrypted = encryptor.decrypt(encrypted);

        System.out.println("Encrypted: " + encrypted);
        System.out.println("Decrypted: " + decrypted);
    }
}
```

**Notes:**

* `Encryptors.text` is simple but sufficient for non-critical text.
* For stronger security, use `Encryptors.standard(password, salt)` which provides AES-based encryption.

---

## **5. When to use `spring-security-crypto`**

* Hashing and storing passwords securely.
* Encrypting configuration secrets or sensitive text in your application.
* Projects that need cryptography without pulling in the full Spring Security dependency.

---