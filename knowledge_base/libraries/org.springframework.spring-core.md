`org.springframework:spring-core` is one of the fundamental modules of the **Spring Framework**. It provides the essential building blocks for all Spring applications, including **dependency injection (DI), resource management, utility classes, and basic APIs** that other Spring modules rely on. Essentially, it’s the “core” of Spring.

Here’s a short guide:

---

## 1. Maven / Gradle Dependency

**Maven:**

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>6.2.5</version> <!-- use the version you need -->
</dependency>
```

**Gradle:**

```gradle
implementation 'org.springframework:spring-core:6.2.5'
```

---

## 2. Key Features of `spring-core`

1. **Dependency Injection (DI)** – Provides `BeanFactory` and `ApplicationContext` for managing objects and their dependencies.
2. **Resource Abstraction** – Access files, classpath resources, URLs, etc., in a uniform way via `Resource` and `ResourceLoader`.
3. **Utility Classes** – Classes for string manipulation, reflection, collections, type conversion, etc.
4. **Environment & Properties** – `PropertySource` and `Environment` APIs to access configuration values.
5. **Event System** – Allows publishing and listening to application events.
6. **Core Interfaces** – Includes `InitializingBean`, `DisposableBean`, `FactoryBean`, etc., to manage lifecycle callbacks.

---

## 3. Basic Usage Examples

### a) Resource Loading

```java
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import java.io.IOException;
import java.nio.file.Files;

public class ResourceExample {
    public static void main(String[] args) throws IOException {
        Resource resource = new ClassPathResource("data.txt");
        String content = Files.readString(resource.getFile().toPath());
        System.out.println(content);
    }
}
```

This allows you to access files from classpath, filesystem, or URLs without worrying about the underlying implementation.

---

### b) Using Spring Utility Classes

```java
import org.springframework.util.StringUtils;

public class StringUtilsExample {
    public static void main(String[] args) {
        String[] arr = StringUtils.commaDelimitedListToStringArray("apple,banana,orange");
        for (String fruit : arr) {
            System.out.println(fruit);
        }
    }
}
```

---

### c) Dependency Injection with `BeanFactory`

```java
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.xml.XmlBeanFactory;
import org.springframework.core.io.ClassPathResource;

public class DIExample {
    public static void main(String[] args) {
        BeanFactory factory = new XmlBeanFactory(new ClassPathResource("beans.xml"));
        MyService service = (MyService) factory.getBean("myService");
        service.doWork();
    }
}
```

> Note: Modern Spring uses `ApplicationContext` instead of `BeanFactory`, but the DI concept is provided by `spring-core`.

---

### d) Event Publishing

```java
import org.springframework.context.ApplicationEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.SimpleApplicationEventMulticaster;

public class EventExample {
    static class MyEvent extends ApplicationEvent {
        public MyEvent(Object source) { super(source); }
    }

    public static void main(String[] args) {
        SimpleApplicationEventMulticaster multicaster = new SimpleApplicationEventMulticaster();
        multicaster.addApplicationListener((ApplicationListener<MyEvent>) event ->
            System.out.println("Received event: " + event)
        );
        multicaster.multicastEvent(new MyEvent("Hello Spring Event!"));
    }
}
```

---

### 4. Notes

* `spring-core` **does not start Spring applications** by itself — it provides the building blocks for other modules like `spring-context`, `spring-beans`, and `spring-aop`.
* Most Spring projects will include `spring-core` automatically via `spring-context`.

---