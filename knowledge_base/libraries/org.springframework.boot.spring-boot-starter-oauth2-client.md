The dependency **Spring Boot `org.springframework.boot:spring-boot-starter-oauth2-client`** is a starter that enables **OAuth2 / OpenID Connect client support** in **Spring Security** applications.

It is used when your application **acts as an OAuth2 client** and needs to:

* log users in via external providers (SSO)
* obtain access tokens
* call protected APIs on behalf of the user

Typical providers include **Keycloak**, **Google OAuth 2.0**, **GitHub OAuth**, etc.

---

# Spring Boot OAuth2 Client – Quick Guide

## 1. Add Dependency

### Maven

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>
```

### Gradle

```gradle
implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
```

This automatically brings:

* Spring Security
* OAuth2 Client libraries
* OIDC support

---

# 2. Configure OAuth2 Client

Configuration is usually done in `application.yml`.

Example with **Keycloak**:

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: my-client
            client-secret: my-secret
            scope: openid,profile,email
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"

        provider:
          keycloak:
            issuer-uri: https://auth.example.com/realms/myrealm
```

Spring will automatically discover:

* authorization endpoint
* token endpoint
* JWK keys

from the issuer.

---

# 3. Enable Login via OAuth2

Minimal configuration:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()
            )
            .oauth2Login();

        return http.build();
    }
}
```

Now when a user opens your application:

```
GET / -> redirect to OAuth provider login
```

---

# 4. Access Logged-In User

Spring injects the authenticated user.

```java
@GetMapping("/user")
public Map<String, Object> user(@AuthenticationPrincipal OAuth2User user) {
    return user.getAttributes();
}
```

For **OIDC**:

```java
@GetMapping("/user")
public String user(@AuthenticationPrincipal OidcUser user) {
    return user.getEmail();
}
```

---

# 5. Access OAuth2 Access Token

Sometimes you need the token to call another service.

```java
@GetMapping("/token")
public String token(
        @RegisteredOAuth2AuthorizedClient("keycloak")
        OAuth2AuthorizedClient client) {

    return client.getAccessToken().getTokenValue();
}
```

---

# 6. Calling Another API with Token

You can attach the token automatically.

Example using `WebClient`:

```java
@Bean
WebClient webClient(OAuth2AuthorizedClientManager manager) {
    ServletOAuth2AuthorizedClientExchangeFilterFunction oauth =
        new ServletOAuth2AuthorizedClientExchangeFilterFunction(manager);

    oauth.setDefaultOAuth2AuthorizedClient(true);

    return WebClient.builder()
        .apply(oauth.oauth2Configuration())
        .build();
}
```

Usage:

```java
webClient.get()
        .uri("https://api.example.com/data")
        .retrieve()
        .bodyToMono(String.class);
```

The access token will be added automatically.

---

# Typical Architecture

```
User
  ↓
Spring Boot App (OAuth2 Client)
  ↓
OAuth Provider (Keycloak / Google)
  ↓
Access Token
  ↓
Call Protected APIs
```

---

# When to Use This Starter

Use `spring-boot-starter-oauth2-client` when your service:

✔ implements **SSO login**
✔ authenticates users via external IdP
✔ calls APIs with OAuth2 tokens
✔ integrates with **Keycloak / Auth0 / Google**

Do **NOT** use it when your service is a **resource server** (validating JWT tokens from other services).
In that case use:

```
spring-boot-starter-oauth2-resource-server
```

---

✅ **Typical microservice setup**

| Service            | Dependency             |
| ------------------ | ---------------------- |
| Frontend / Gateway | oauth2-client          |
| Backend APIs       | oauth2-resource-server |
| Identity Provider  | Keycloak               |
