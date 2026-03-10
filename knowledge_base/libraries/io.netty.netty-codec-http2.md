## Guide: Using `io.netty:netty-codec-http2`

### 1. What is `netty-codec-http2`

`netty-codec-http2` is a module from the Netty project that implements the **HTTP/2 protocol**.

It provides:

* HTTP/2 frame encoding/decoding
* stream multiplexing
* flow control
* header compression (HPACK)
* server push support

Unlike HTTP/1.1, **HTTP/2 runs multiple request/response streams over a single TCP connection**, improving performance and reducing latency.

`netty-codec-http2` allows you to build:

* HTTP/2 servers
* HTTP/2 clients
* gRPC servers
* high-performance API gateways

It is used internally by frameworks like gRPC.

---

# 2. Add Dependency

### Maven

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-codec-http2</artifactId>
    <version>4.1.108.Final</version>
</dependency>
```

You will typically also use:

```
netty-transport
netty-handler
netty-codec-http
```

---

# 3. HTTP/2 Core Concepts

HTTP/2 introduces several new concepts:

| Concept          | Description                          |
| ---------------- | ------------------------------------ |
| **Connection**   | Single TCP connection                |
| **Stream**       | Independent request/response channel |
| **Frame**        | Binary protocol message              |
| **Multiplexing** | Many streams on one connection       |
| **HPACK**        | Header compression                   |

Example flow:

```
TCP Connection
   ├── Stream 1 (request/response)
   ├── Stream 3 (request/response)
   ├── Stream 5 (request/response)
```

---

# 4. Key Netty HTTP/2 Classes

Important classes in `netty-codec-http2`:

| Class                   | Purpose                      |
| ----------------------- | ---------------------------- |
| `Http2FrameCodec`       | HTTP/2 frame encoder/decoder |
| `Http2MultiplexHandler` | Handles multiple streams     |
| `Http2Headers`          | HTTP/2 headers               |
| `Http2StreamChannel`    | Channel per stream           |
| `Http2FrameListener`    | Low-level frame handling     |

Most applications use:

```
Http2FrameCodec
Http2MultiplexHandler
```

---

# 5. Basic HTTP/2 Server Example

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

            Http2FrameCodec codec = Http2FrameCodecBuilder.forServer().build();

            p.addLast(codec);

            p.addLast(new Http2MultiplexHandler(new Http2StreamHandler()));
        }
    });

bootstrap.bind(8080).sync();
```

Pipeline:

```
Socket
   ↓
Http2FrameCodec
   ↓
Http2MultiplexHandler
   ↓
Stream Handlers
```

---

# 6. Stream Request Handler

Each HTTP request is handled in a **separate stream channel**.

```java
public class Http2StreamHandler extends ChannelInboundHandlerAdapter {

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {

        if (msg instanceof Http2HeadersFrame headersFrame) {

            Http2Headers headers = headersFrame.headers();

            if (headersFrame.isEndStream()) {
                sendResponse(ctx);
            }
        }
    }

    private void sendResponse(ChannelHandlerContext ctx) {

        Http2Headers headers = new DefaultHttp2Headers()
            .status("200")
            .set("content-type", "text/plain");

        ctx.write(new DefaultHttp2HeadersFrame(headers, false));

        ByteBuf content = ctx.alloc().buffer();
        content.writeBytes("Hello HTTP/2".getBytes());

        ctx.writeAndFlush(new DefaultHttp2DataFrame(content, true));
    }
}
```

---

# 7. Handling Request Headers

HTTP/2 headers are binary and use pseudo-headers.

Example:

```
:method = GET
:path = /hello
:scheme = https
:authority = example.com
```

Accessing them:

```java
String path = headers.path().toString();
String method = headers.method().toString();
```

---

# 8. HTTP/2 with TLS (Recommended)

Most HTTP/2 deployments run over TLS.

Typical pipeline:

```
SslHandler
Http2FrameCodec
Http2MultiplexHandler
StreamHandler
```

TLS setup example:

```java
SslContext sslContext = SslContextBuilder.forServer(cert, key)
    .applicationProtocolConfig(
        new ApplicationProtocolConfig(
            Protocol.ALPN,
            SelectorFailureBehavior.NO_ADVERTISE,
            SelectedListenerFailureBehavior.ACCEPT,
            ApplicationProtocolNames.HTTP_2))
    .build();
```

ALPN negotiation selects HTTP/2 automatically.

---

# 9. Supporting HTTP/1.1 and HTTP/2

Many servers support **both protocols**.

Netty provides:

```
ApplicationProtocolNegotiationHandler
```

Example flow:

```
TLS Handshake
      ↓
ALPN negotiation
      ↓
HTTP/2 or HTTP/1.1 pipeline
```

---

# 10. Typical Production Pipeline

A real HTTP/2 Netty server might look like:

```
SslHandler
ApplicationProtocolNegotiationHandler
Http2FrameCodec
Http2MultiplexHandler
LoggingHandler
BusinessHandler
```

Features enabled:

* multiplexing
* header compression
* TLS
* stream isolation

---

# 11. When to Use `netty-codec-http2`

Use it when building:

| System                          | Why                   |
| ------------------------------- | --------------------- |
| gRPC servers                    | HTTP/2 required       |
| high-performance API gateways   | multiplexing          |
| streaming APIs                  | bidirectional streams |
| internal microservice protocols | efficient connections |

Many modern systems rely on HTTP/2 for efficient communication.

---

# 12. Common Pitfalls

### 1️⃣ Streams vs Connections

HTTP/2 multiplexes streams:

```
Connection
  ├ stream 1
  ├ stream 3
  └ stream 5
```

Your handler must be **stream-aware**.

---

### 2️⃣ Flow Control

HTTP/2 includes **flow control windows**.

Large responses may stall if the window is exceeded.

---

### 3️⃣ Incorrect pipeline order

Wrong:

```
Http2FrameCodec
SslHandler
```

Correct:

```
SslHandler
Http2FrameCodec
```

---

# 13. When NOT to Use It

Avoid using raw Netty HTTP/2 if you only need REST APIs.

Use frameworks like:

* Spring Boot
* Micronaut
* Quarkus

Use `netty-codec-http2` when:

✔ building infrastructure components
✔ implementing custom protocols
✔ building gRPC infrastructure
✔ optimizing network performance

---

✅ **Summary**

`netty-codec-http2` enables **HTTP/2 protocol support in Netty**, providing multiplexed streams, binary framing, and high-performance communication.

Core components:

```
Http2FrameCodec
Http2MultiplexHandler
Http2HeadersFrame
Http2DataFrame
Http2StreamChannel
```

It is a foundation for building **modern high-throughput networking systems** on top of Netty.