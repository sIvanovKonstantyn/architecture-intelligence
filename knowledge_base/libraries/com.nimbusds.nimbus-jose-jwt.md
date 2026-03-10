**`com.nimbusds:nimbus-jose-jwt`** is a popular Java library for working with **JWT (JSON Web Tokens)** and **JOSE standards**:

* **JWS** – JSON Web Signature (signed tokens)
* **JWE** – JSON Web Encryption (encrypted tokens)
* **JWT** – JSON Web Tokens
* **JWK** – JSON Web Keys

It’s widely used in **OAuth2 / OpenID Connect**, security gateways, and identity providers (including integrations with things like Keycloak and Spring Security).

GitHub: [https://github.com/connect2id/nimbus-jose-jwt](https://github.com/connect2id/nimbus-jose-jwt)

---

# 1. Add Dependency

Maven:

```xml
<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>nimbus-jose-jwt</artifactId>
    <version>9.37</version>
</dependency>
```

Gradle:

```gradle
implementation 'com.nimbusds:nimbus-jose-jwt:9.37'
```

---

# 2. Creating a Signed JWT

Example: create a **JWT signed with HMAC SHA256**.

```java
import com.nimbusds.jose.*;
import com.nimbusds.jose.crypto.*;
import com.nimbusds.jwt.*;

import java.util.Date;

public class JwtExample {

    public static void main(String[] args) throws Exception {

        // Create JWT claims
        JWTClaimsSet claimsSet = new JWTClaimsSet.Builder()
                .subject("user123")
                .issuer("my-app")
                .expirationTime(new Date(new Date().getTime() + 60 * 1000))
                .claim("role", "admin")
                .build();

        // Create signer
        JWSSigner signer = new MACSigner("super-secret-key-which-is-long".getBytes());

        SignedJWT signedJWT = new SignedJWT(
                new JWSHeader(JWSAlgorithm.HS256),
                claimsSet
        );

        // Sign the JWT
        signedJWT.sign(signer);

        String token = signedJWT.serialize();

        System.out.println(token);
    }
}
```

Result: standard **JWT string**

```
header.payload.signature
```

---

# 3. Parsing and Verifying JWT

Example: verify a received token.

```java
import com.nimbusds.jose.crypto.MACVerifier;
import com.nimbusds.jwt.SignedJWT;

SignedJWT signedJWT = SignedJWT.parse(token);

boolean verified = signedJWT.verify(
        new MACVerifier("super-secret-key-which-is-long".getBytes())
);

if (verified) {
    String subject = signedJWT.getJWTClaimsSet().getSubject();
    System.out.println("User: " + subject);
}
```

---

# 4. Reading JWT Claims

```java
JWTClaimsSet claims = signedJWT.getJWTClaimsSet();

String subject = claims.getSubject();
Date expiration = claims.getExpirationTime();
String role = claims.getStringClaim("role");
```

Typical claims:

| Claim | Meaning           |
| ----- | ----------------- |
| `sub` | subject (user id) |
| `iss` | issuer            |
| `exp` | expiration        |
| `iat` | issued at         |
| `aud` | audience          |

---

# 5. Using RSA Keys (Typical for OAuth2)

Example: **RS256 signing**

```java
JWSSigner signer = new RSASSASigner(privateKey);

SignedJWT jwt = new SignedJWT(
        new JWSHeader(JWSAlgorithm.RS256),
        claims
);

jwt.sign(signer);
```

Verification:

```java
JWSVerifier verifier = new RSASSAVerifier(publicKey);

boolean valid = jwt.verify(verifier);
```

This is how **identity providers** issue tokens.

---

# 6. Working with JWK (JSON Web Keys)

Libraries like Keycloak or Auth0 expose **JWKS endpoints**.

Nimbus can load them:

```java
JWKSet jwkSet = JWKSet.load(new URL("https://example.com/.well-known/jwks.json"));

JWK key = jwkSet.getKeys().get(0);
RSAKey rsaKey = (RSAKey) key;
```

Then verify JWT with the public key.

---

# 7. JWT Processing Pipeline

Typical flow:

```
Client
   ↓
Authorization Server
   ↓ issues JWT
API Gateway
   ↓ verifies JWT
Microservice
   ↓ reads claims
Business Logic
```

`nimbus-jose-jwt` usually handles:

* token **verification**
* **signature validation**
* **claim parsing**

---

# 8. Typical Spring Boot Usage

Often used inside:

* custom **JWT filters**
* **OAuth2 resource servers**
* **API gateways**

Example:

```java
SignedJWT jwt = SignedJWT.parse(authHeaderToken);

if (!jwt.verify(verifier)) {
    throw new SecurityException("Invalid token");
}
```

---

# 9. Why Nimbus is Popular

Pros:

✔ full **JOSE standard support**
✔ widely used in **OAuth2 / OIDC**
✔ supports **JWS, JWE, JWK, JWT**
✔ high performance
✔ used by many frameworks internally

Many frameworks (including parts of Spring Security) rely on it under the hood.

---

✅ **In short**

`nimbus-jose-jwt` is a **low-level Java toolkit for JWT and JOSE standards**, giving you full control over:

* token signing
* verification
* encryption
* JWK key management