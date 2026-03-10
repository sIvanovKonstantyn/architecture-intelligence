`org.springframework.boot:spring-boot-devtools` is a Spring Boot module that provides **development-time features** to improve productivity when building Spring Boot applications. Its main goal is to make the development cycle faster and easier, without affecting production.

Here’s a concise guide:

---

## Key Features

1. **Automatic Restart**

   * DevTools watches your classpath for changes and **restarts the application automatically**.
   * Only application classes are reloaded, while static resources like `application.properties` may be re-read without a full restart.

2. **LiveReload Support**

   * Integrated LiveReload server refreshes your browser automatically when resources change.
   * Works well with Thymeleaf, HTML, CSS, JS changes.

3. **Property Defaults for Development**

   * DevTools enables sensible defaults for development, e.g., `spring.thymeleaf.cache=false` to disable template caching.

4. **Remote Debug Support**

   * You can enable remote development with `spring-boot-devtools` to restart apps running on remote machines.

5. **Excludes from Restart**

   * You can exclude libraries or classes from triggering a restart (like large dependencies).

---

## How to Use

### 1. Add Dependency

**Maven**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <optional>true</optional>
</dependency>
```

**Gradle**

```gradle
dependencies {
    developmentOnly("org.springframework.boot:spring-boot-devtools")
}
```

> Note: It’s recommended to mark it as **optional** in Maven or `developmentOnly` in Gradle so it doesn’t get included in your production build.

---

### 2. Enable Automatic Restart

* DevTools watches `src/main/java` and `src/main/resources` for changes.
* Save a file → Spring Boot automatically restarts.
* To avoid restarting for some changes (like static libraries), configure:

```properties
spring.devtools.restart.exclude=static/**,public/**
spring.devtools.restart.enabled=true
```

---

### 3. Enable LiveReload

* By default, DevTools starts a LiveReload server on port 35729.
* Install a browser plugin (LiveReload) or use an IDE integration.
* When you save changes to HTML/CSS/JS → browser refreshes automatically.

---

### 4. Customize Behavior

```properties
# Disable automatic restart
spring.devtools.restart.enabled=false

# Watch additional directories
spring.devtools.restart.additional-paths=src/main/webapp

# Set LiveReload to false if not needed
spring.devtools.livereload.enabled=false
```

---

### 5. Tips

* Works best in **development mode only**. Avoid including in production.
* For large projects, automatic restart may slow down. You can use **trigger files** to control restarts manually.
* DevTools does **not replace hot code replacement** from your IDE (e.g., IntelliJ or Eclipse Hotswap), but complements it.

---

💡 **Example Workflow**

1. Run Spring Boot app with DevTools.
2. Edit a controller or template.
3. Save → app restarts automatically.
4. Browser reloads automatically (LiveReload).
5. Test changes immediately without manual restart.