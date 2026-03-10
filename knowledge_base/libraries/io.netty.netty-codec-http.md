## Guide: Using `io.netty:netty-codec-http`

### 1. What is `netty-codec-http`

`netty-codec-http` is a module from the Netty framework that provides **HTTP protocol encoding and decoding**.

It converts **raw TCP bytes** into **HTTP objects** and vice versa.

In simple terms:

```
TCP Bytes  <->  HTTP Decoder/Encoder  <->  HTTP Objects
```

The module allows you to build:

* HTTP servers
* HTTP clients
* API gateways
* reverse proxies
* WebSocket servers

without relying on heavyweight frameworks like Spring Boot.

---

# 2. Add Dependency

### Maven

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-codec-http</artifactId>
    <version>4.1.108.Final</version>
</dependency>
```

Usually it is used together with:

```
netty-transport
netty-handler
netty-buffer
```

or simply:

```
netty-all
```

---

# 3. Key HTTP Classes

Important classes provided by `netty-codec-http`:

| Class                  | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `HttpServerCodec`      | HTTP encoder + decoder                    |
| `HttpObjectAggregator` | Combines HTTP chunks into FullHttpRequest |
| `FullHttpRequest`      | Complete HTTP request                     |
| `FullHttpResponse`     | Complete HTTP response                    |
| `HttpHeaders`          | HTTP headers                              |
| `HttpMethod`           | HTTP method enum                          |
| `QueryStringDecoder`   | Parses URL parameters                     |

---

# 4. Minimal HTTP Server Example

### Step 1 — Server Bootstrap

```java
EventLoopGroup boss = new NioEventLoopGroup(1);
EventLoopGroup worker = new NioEventLoopGroup();

ServerBootstrap bootstrap = new ServerBootstrap();

bootstrap.group(boss, worker)
    .channel(NioServerSocketChannel.class)
    .childHandler(new ChannelInitializer<SocketChannel>() {
        @Override
        protected void initChannel(SocketChannel ch) {

            ChannelPipeline p = ch.pipeline();

            p.addLast(new HttpServerCodec());
            p.addLast(new HttpObjectAggregator(65536));
            p.addLast(new HttpHandler());
        }
    });

bootstrap.bind(8080).sync();
```

Pipeline:

```
Socket
   ↓
HttpServerCodec
   ↓
HttpObjectAggregator
   ↓
Your Handler
```

---

# 5. HTTP Request Handler

```java
public class HttpHandler extends SimpleChannelInboundHandler<FullHttpRequest> {

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, FullHttpRequest request) {

        String content = "Hello Netty HTTP";

        FullHttpResponse response =
            new DefaultFullHttpResponse(
                HttpVersion.HTTP_1_1,
                HttpResponseStatus.OK,
                Unpooled.copiedBuffer(content.getBytes())
            );

        response.headers().set(HttpHeaderNames.CONTENT_TYPE, "text/plain");
        response.headers().set(HttpHeaderNames.CONTENT_LENGTH, content.length());

        ctx.writeAndFlush(response);
    }
}
```

Test:

```
curl http://localhost:8080
```

Response:

```
Hello Netty HTTP
```

---

# 6. Handling Query Parameters

Example request:

```
GET /hello?name=John
```

Use `QueryStringDecoder`.

```java
QueryStringDecoder decoder = new QueryStringDecoder(request.uri());

Map<String, List<String>> params = decoder.parameters();

String name = params.getOrDefault("name", List.of("guest")).get(0);
```

---

# 7. Reading Request Body

For POST requests:

```java
String body = request.content().toString(StandardCharsets.UTF_8);
```

Example JSON request:

```
POST /api
Content-Type: application/json

{"name":"John"}
```

---

# 8. Returning JSON Response

```java
String json = "{\"status\":\"ok\"}";

FullHttpResponse response =
    new DefaultFullHttpResponse(
        HttpVersion.HTTP_1_1,
        HttpResponseStatus.OK,
        Unpooled.copiedBuffer(json, StandardCharsets.UTF_8)
    );

response.headers().set(HttpHeaderNames.CONTENT_TYPE, "application/json");
response.headers().set(HttpHeaderNames.CONTENT_LENGTH, json.length());
```

---

# 9. Handling Large Requests (Streaming)

If you **do not use `HttpObjectAggregator`**, you receive chunked messages:

```
HttpRequest
HttpContent
HttpContent
LastHttpContent
```

This allows streaming uploads (files, etc).

Handler example:

```java
if (msg instanceof HttpContent) {
    ByteBuf buf = ((HttpContent) msg).content();
}
```

---

# 10. Typical Pipeline in Production

A real Netty HTTP server pipeline usually looks like this:

```
HttpServerCodec
HttpObjectAggregator
HttpContentCompressor
IdleStateHandler
LoggingHandler
YourBusinessHandler
```

Capabilities:

* compression
* idle connection detection
* logging
* streaming

---

# 11. When to Use `netty-codec-http`

Use it when building:

| System                 | Why                   |
| ---------------------- | --------------------- |
| API Gateway            | high throughput       |
| Reverse proxy          | low latency           |
| WebSocket servers      | Netty handles upgrade |
| Async microservices    | event loop model      |
| Custom HTTP frameworks | full control          |

Many high-performance systems are built on top of Netty, including:

* gRPC
* Apache Dubbo
* Elasticsearch

---

# 12. Common Pitfalls

### 1️⃣ Forgetting `HttpObjectAggregator`

Without it:

```
FullHttpRequest != received
```

You get chunked messages instead.

---

### 2️⃣ Memory leaks with ByteBuf

Netty uses **reference-counted buffers**.

Always:

```
SimpleChannelInboundHandler
```

or manually release buffers.

---

### 3️⃣ Blocking event loop

Never do:

```
database call
file IO
sleep()
```

inside Netty handler.

Use:

```
worker thread pool
```

---

# 13. When NOT to Use It

Avoid using raw Netty HTTP if you just need a REST API.

Use:

* Spring Boot
* Micronaut
* Quarkus

Use `netty-codec-http` when:

✔ performance matters
✔ you need custom networking
✔ you build infrastructure components

---

✅ **Summary**

`netty-codec-http` provides the HTTP protocol layer for the Netty networking framework, allowing developers to build **high-performance HTTP servers and clients with full control over the networking pipeline.**

Core components:

```
HttpServerCodec
HttpObjectAggregator
FullHttpRequest
FullHttpResponse
ChannelPipeline
```