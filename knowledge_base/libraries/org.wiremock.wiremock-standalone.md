`org.wiremock:wiremock-standalone` is the standalone version of **WireMock**, a popular Java library for mocking HTTP services. It allows you to run a self-contained HTTP server that simulates APIs for testing purposes, without needing the full application backend. Since it’s “standalone,” you can run it as a **jar** without integrating it as a library into your project, which is useful for integration tests or local testing.

Here’s a concise guide to using it:

---

## 1️⃣ Getting WireMock Standalone

You can download the standalone JAR from [Maven Central](https://search.maven.org/artifact/org.wiremock/wiremock-standalone):

```xml
<dependency>
    <groupId>org.wiremock</groupId>
    <artifactId>wiremock-standalone</artifactId>
    <version>3.2.0</version> <!-- check for latest version -->
    <scope>test</scope>
</dependency>
```

Or download the JAR directly and run it via the command line:

```bash
java -jar wiremock-standalone-3.2.0.jar --port 8080
```

This will start a WireMock server on `http://localhost:8080`.

---

## 2️⃣ Basic Usage

### a) Stubbing a response

WireMock allows you to define **stubs**, which are predefined HTTP responses for specific requests. You can do this via JSON files or using the Java API.

#### Using JSON files

Create a directory `mappings` with JSON files describing stubs:

```json
{
  "request": {
    "method": "GET",
    "url": "/hello"
  },
  "response": {
    "status": 200,
    "body": "Hello, WireMock!"
  }
}
```

Place it under a folder called `mappings` in the same directory as the standalone JAR. WireMock will automatically load it on startup.

#### Using Java API

If you include WireMock in a project:

```java
import static com.github.tomakehurst.wiremock.client.WireMock.*;

public class Example {
    public static void main(String[] args) {
        WireMockServer wireMockServer = new WireMockServer(8080);
        wireMockServer.start();

        configureFor("localhost", 8080);
        stubFor(get(urlEqualTo("/hello"))
                .willReturn(aResponse()
                    .withStatus(200)
                    .withBody("Hello, WireMock!")));

        // keep server running
    }
}
```

---

### b) Verifying requests

You can also verify that a request was made:

```java
verify(getRequestedFor(urlEqualTo("/hello")));
```

---

### c) Dynamic responses

WireMock supports:

* **Response templating** (based on request parameters)
* **Delays** (simulate slow APIs)
* **Faults** (simulate network errors)
* **HTTPS** (self-signed cert support)

Example with a delay:

```json
{
  "request": {
    "method": "GET",
    "url": "/slow"
  },
  "response": {
    "status": 200,
    "body": "Slow response",
    "fixedDelayMilliseconds": 3000
  }
}
```

---

### 3️⃣ Common CLI Options

* `--port 8080` → set HTTP port
* `--https-port 8443` → set HTTPS port
* `--root-dir <dir>` → specify directory for `mappings` and `__files`
* `--verbose` → log incoming requests

Example:

```bash
java -jar wiremock-standalone-3.2.0.jar --port 8080 --root-dir ./wiremock
```

Directory structure:

```
wiremock/
  mappings/
    hello.json
  __files/
    response-file.txt
```

---

### ✅ Summary

* WireMock Standalone is a self-contained mock HTTP server.
* Supports stubbing, request verification, delays, and faults.
* Can be run via JAR or embedded in Java tests.
* Ideal for integration testing or simulating unavailable APIs.

---