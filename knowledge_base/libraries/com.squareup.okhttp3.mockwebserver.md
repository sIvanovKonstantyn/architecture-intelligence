**`com.squareup.okhttp3.mockwebserver`** is a testing utility from the Square, Inc. networking library OkHttp.
It allows you to run a **local HTTP server in tests** and **control exactly what responses your HTTP client receives**.

It is widely used to test **HTTP clients, integrations, and retry logic** without calling real external services.

---

# Quick Guide: Using `MockWebServer`

## 1. Add dependency

**Maven**

```xml
<dependency>
  <groupId>com.squareup.okhttp3</groupId>
  <artifactId>mockwebserver</artifactId>
  <version>4.12.0</version>
  <scope>test</scope>
</dependency>
```

**Gradle**

```gradle
testImplementation("com.squareup.okhttp3:mockwebserver:4.12.0")
```

---

# 2. Basic idea

`MockWebServer` works like this:

1. Start a local HTTP server.
2. Enqueue predefined responses.
3. Execute your client call.
4. Verify the request and response.

Flow:

```
Test → MockWebServer → Your HTTP client
```

---

# 3. Minimal Example

```java
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class HttpClientTest {

    @Test
    void testCall() throws Exception {

        MockWebServer server = new MockWebServer();

        server.enqueue(new MockResponse()
                .setBody("{\"status\":\"ok\"}")
                .setResponseCode(200));

        server.start();

        OkHttpClient client = new OkHttpClient();

        String baseUrl = server.url("/api/status").toString();

        Request request = new Request.Builder()
                .url(baseUrl)
                .build();

        Response response = client.newCall(request).execute();

        assertEquals(200, response.code());

        server.shutdown();
    }
}
```

---

# 4. Verifying Requests

You can inspect what the client actually sent.

```java
RecordedRequest request = server.takeRequest();

assertEquals("/api/status", request.getPath());
assertEquals("GET", request.getMethod());
```

This is very useful for testing:

* headers
* query parameters
* authentication
* payloads

---

# 5. Mocking JSON API Responses

Example for a REST API test.

```java
server.enqueue(
    new MockResponse()
        .setHeader("Content-Type", "application/json")
        .setBody("""
            {
              "price": 65000,
              "currency": "BTC"
            }
        """)
);
```

Your client will receive this **exact response**.

---

# 6. Testing Error Handling

Simulate API failures.

### 500 error

```java
server.enqueue(new MockResponse().setResponseCode(500));
```

### Timeout

```java
server.enqueue(
    new MockResponse()
        .setBody("slow response")
        .setBodyDelay(5, TimeUnit.SECONDS)
);
```

### Connection drop

```java
server.enqueue(
    new MockResponse()
        .setSocketPolicy(SocketPolicy.DISCONNECT_AFTER_REQUEST)
);
```

This is extremely useful for testing **retry logic**.

---

# 7. Testing Multiple Requests

You can queue multiple responses.

```java
server.enqueue(new MockResponse().setResponseCode(500));
server.enqueue(new MockResponse().setResponseCode(200));
```

Your client will receive:

1️⃣ 500
2️⃣ 200

Perfect for **retry tests**.

---

# 8. JUnit Integration Example

```java
class ApiTest {

    private MockWebServer server;

    @BeforeEach
    void setup() throws IOException {
        server = new MockWebServer();
        server.start();
    }

    @AfterEach
    void teardown() throws IOException {
        server.shutdown();
    }

}
```

---

# 9. Best Practices

### Use dynamic base URL

Always inject server URL:

```java
String baseUrl = server.url("/").toString();
```

Avoid hardcoded URLs.

---

### Store JSON in files

Instead of inline strings:

```
src/test/resources/responses/user.json
```

Load in test.

---

### Verify requests

Always check:

* path
* headers
* payload

Example:

```java
assertEquals("Bearer token", request.getHeader("Authorization"));
```

---

# 10. When to Use `MockWebServer`

Good for testing:

* HTTP clients
* REST integrations
* retry logic
* rate limit handling
* error scenarios

Not ideal for:

* full system integration tests
* contract testing between services

---

# Summary

`MockWebServer` gives you:

✔ deterministic HTTP tests
✔ no external dependencies
✔ full request inspection
✔ simulation of network failures

It is one of the **best tools for testing HTTP integrations in Java**.