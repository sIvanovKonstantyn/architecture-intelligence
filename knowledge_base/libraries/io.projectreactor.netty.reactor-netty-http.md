**`io.projectreactor.netty:reactor-netty-http`** is a module of **Reactor Netty** that provides **non-blocking HTTP client and server implementations built on top of Netty and the reactive programming model from Project Reactor**.

It is commonly used internally by frameworks like **Spring WebFlux** as the default HTTP runtime.

In simple terms, it lets you build **reactive HTTP servers and clients** using `Mono` and `Flux`.

---

# 1. Dependency

### Maven

```xml
<dependency>
    <groupId>io.projectreactor.netty</groupId>
    <artifactId>reactor-netty-http</artifactId>
    <version>1.1.17</version>
</dependency>
```

### Gradle

```gradle
implementation 'io.projectreactor.netty:reactor-netty-http:1.1.17'
```

---

# 2. Key Concepts

Main classes you will use:

| Class        | Purpose                |
| ------------ | ---------------------- |
| `HttpServer` | Reactive HTTP server   |
| `HttpClient` | Reactive HTTP client   |
| `Mono`       | async single value     |
| `Flux`       | async stream of values |

The API is **fully asynchronous and non-blocking**.

---

# 3. Creating a Simple HTTP Server

Example: minimal HTTP server.

```java
import reactor.netty.http.server.HttpServer;
import reactor.core.publisher.Mono;

public class ServerExample {

    public static void main(String[] args) {
        HttpServer.create()
                .port(8080)
                .route(routes ->
                        routes.get("/hello",
                                (request, response) ->
                                        response.sendString(Mono.just("Hello Reactive World")))
                )
                .bindNow()
                .onDispose()
                .block();
    }
}
```

### What happens here

1. `HttpServer.create()` — creates server.
2. `route()` — registers handlers.
3. `sendString()` — returns reactive response.
4. `bindNow()` — starts server.

Request flow:

```
HTTP request
   ↓
Netty event loop
   ↓
Reactor handler (Mono/Flux)
   ↓
Reactive response
```

---

# 4. Handling Request Body

Example: echo endpoint.

```java
HttpServer.create()
    .port(8080)
    .route(routes ->
        routes.post("/echo", (req, res) ->
            res.send(
                req.receive()
                   .retain()
            )
        )
    )
    .bindNow();
```

`req.receive()` returns a **Flux of ByteBuf**.

---

# 5. Creating an HTTP Client

Example request:

```java
import reactor.netty.http.client.HttpClient;

public class ClientExample {

    public static void main(String[] args) {

        String response =
            HttpClient.create()
                .get()
                .uri("https://httpbin.org/get")
                .responseContent()
                .aggregate()
                .asString()
                .block();

        System.out.println(response);
    }
}
```

Flow:

```
HttpClient
   ↓
Reactive pipeline
   ↓
Netty async IO
   ↓
Mono<String> response
```

---

# 6. Non-Blocking Streaming

One advantage of Reactor Netty is **streaming responses**.

Example:

```java
HttpClient.create()
    .get()
    .uri("https://example.com/stream")
    .responseContent()
    .asString()
    .subscribe(System.out::println);
```

Here:

* data is processed **as it arrives**
* no full buffering required.

---

# 7. Connection Configuration

Example:

```java
HttpClient client =
    HttpClient.create()
        .compress(true)
        .followRedirect(true)
        .responseTimeout(Duration.ofSeconds(5));
```

Useful options:

| Setting             | Description      |
| ------------------- | ---------------- |
| `responseTimeout()` | request timeout  |
| `compress(true)`    | enable gzip      |
| `keepAlive(true)`   | connection reuse |
| `wiretap(true)`     | debug logging    |

---

# 8. Connection Pooling

Reactor Netty provides connection pooling.

```java
ConnectionProvider provider =
        ConnectionProvider.builder("custom")
                .maxConnections(100)
                .pendingAcquireTimeout(Duration.ofSeconds(60))
                .build();

HttpClient client = HttpClient.create(provider);
```

---

# 9. TLS / HTTPS

Example:

```java
HttpClient.create()
    .secure()
    .get()
    .uri("https://api.example.com")
```

---

# 10. When to Use Reactor Netty

Use it when you need:

✅ high-performance HTTP client
✅ reactive backpressure support
✅ streaming APIs
✅ event-driven networking
✅ integration with WebFlux

Typical use cases:

* API gateways
* microservice HTTP clients
* streaming services
* reactive backends

---

# 11. When NOT to Use It

Avoid if:

* you need simple synchronous HTTP → use `HttpURLConnection` or `RestTemplate`
* you are not using reactive programming
* you want simpler APIs

---

💡 **Real-world usage**

Many frameworks rely on Reactor Netty internally:

* Spring WebFlux (default runtime)
* Spring Cloud Gateway
* reactive microservices on **Spring Boot**

---

✅ **Summary**

`reactor-netty-http` provides:

* reactive HTTP server
* reactive HTTP client
* non-blocking networking
* high scalability with Netty event loops

Architecture:

```
Application
   ↓
Project Reactor (Mono / Flux)
   ↓
Reactor Netty
   ↓
Netty
   ↓
TCP
```