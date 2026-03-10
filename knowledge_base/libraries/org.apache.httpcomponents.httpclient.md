**`org.apache.httpcomponents.httpclient`** is a Java library from the Apache Software Foundation that provides a flexible and powerful HTTP client for sending HTTP requests and handling responses.
It is part of the Apache HttpComponents HttpClient project and was widely used before the introduction of the built-in Java HttpClient.

It supports:

* HTTP/HTTPS requests
* connection pooling
* authentication
* cookies
* redirects
* streaming large responses
* retry and timeout configuration

---

# 1. Dependency

### Maven (HttpClient 4.x)

```xml
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.14</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.apache.httpcomponents:httpclient:4.5.14'
```

---

# 2. Basic Concepts

Main classes:

| Class                                          | Purpose                  |
| ---------------------------------------------- | ------------------------ |
| `CloseableHttpClient`                          | Main HTTP client         |
| `HttpGet`, `HttpPost`, `HttpPut`, `HttpDelete` | HTTP request types       |
| `HttpResponse`                                 | Server response          |
| `HttpEntity`                                   | Response or request body |
| `HttpClientBuilder`                            | Client configuration     |

---

# 3. Simple GET Request

```java
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.util.EntityUtils;

public class Example {

    public static void main(String[] args) throws Exception {

        try (CloseableHttpClient client = HttpClients.createDefault()) {

            HttpGet request = new HttpGet("https://api.example.com/data");

            try (CloseableHttpResponse response = client.execute(request)) {

                int status = response.getStatusLine().getStatusCode();
                String body = EntityUtils.toString(response.getEntity());

                System.out.println(status);
                System.out.println(body);
            }
        }
    }
}
```

Steps:

1. Create `CloseableHttpClient`
2. Create request (`HttpGet`)
3. Execute request
4. Read response
5. Close resources

---

# 4. POST Request with JSON

```java
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.client.methods.CloseableHttpResponse;

HttpPost request = new HttpPost("https://api.example.com/users");

request.setHeader("Content-Type", "application/json");

String json = "{\"name\":\"John\"}";
request.setEntity(new StringEntity(json));

try (CloseableHttpClient client = HttpClients.createDefault();
     CloseableHttpResponse response = client.execute(request)) {

    System.out.println(response.getStatusLine());
}
```

---

# 5. Adding Headers

```java
request.setHeader("Authorization", "Bearer TOKEN");
request.setHeader("Accept", "application/json");
```

or

```java
request.addHeader("X-Request-ID", "123");
```

---

# 6. Handling Query Parameters

```java
URI uri = new URIBuilder("https://api.example.com/search")
        .addParameter("q", "java")
        .addParameter("limit", "10")
        .build();

HttpGet request = new HttpGet(uri);
```

---

# 7. Timeouts Configuration

```java
RequestConfig config = RequestConfig.custom()
        .setConnectTimeout(5000)
        .setSocketTimeout(5000)
        .setConnectionRequestTimeout(5000)
        .build();

CloseableHttpClient client = HttpClients.custom()
        .setDefaultRequestConfig(config)
        .build();
```

Types of timeouts:

| Timeout                    | Meaning                               |
| -------------------------- | ------------------------------------- |
| connect timeout            | time to establish connection          |
| socket timeout             | time waiting for data                 |
| connection request timeout | time waiting for connection from pool |

---

# 8. Connection Pooling (Important for Production)

```java
PoolingHttpClientConnectionManager cm =
        new PoolingHttpClientConnectionManager();

cm.setMaxTotal(100);
cm.setDefaultMaxPerRoute(20);

CloseableHttpClient client = HttpClients.custom()
        .setConnectionManager(cm)
        .build();
```

Benefits:

* reuse TCP connections
* improve performance
* reduce latency

---

# 9. Retry Strategy

```java
HttpRequestRetryHandler retryHandler = (exception, executionCount, context) -> {
    return executionCount < 3;
};

CloseableHttpClient client = HttpClients.custom()
        .setRetryHandler(retryHandler)
        .build();
```

---

# 10. Best Practices

✔ Reuse a single `HttpClient` instance
✔ Use connection pooling
✔ Always close `HttpResponse`
✔ Configure timeouts
✔ Use streaming for large responses

Avoid:

❌ Creating a new client per request
❌ Not closing entities
❌ Ignoring timeouts

---

# 11. HttpClient 4 vs 5

There are two major versions:

| Version | Package             |
| ------- | ------------------- |
| 4.x     | `org.apache.http.*` |
| 5.x     | `org.apache.hc.*`   |

Example new dependency:

```xml
<dependency>
  <groupId>org.apache.httpcomponents.client5</groupId>
  <artifactId>httpclient5</artifactId>
  <version>5.3</version>
</dependency>
```

---

# 12. When to Use It Today

Use cases:

* legacy Spring applications
* advanced HTTP configuration
* custom retry/pooling logic

But modern alternatives include:

* Java HttpClient (built-in)
* Spring WebClient
* OkHttp