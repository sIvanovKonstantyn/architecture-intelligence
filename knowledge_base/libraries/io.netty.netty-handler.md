## Guide: Using `io.netty:netty-handler`

### 1. What is `netty-handler`

`netty-handler` is a module of the Netty that provides **ready-to-use ChannelHandlers for common networking tasks** such as:

* SSL/TLS support
* idle connection detection
* logging
* traffic shaping
* timeout handling
* compression
* protocol upgrades

While `netty-codec` focuses on **encoding and decoding messages**, `netty-handler` provides **middleware-like handlers** that sit inside the **Netty pipeline** and manage connection behavior.

Typical pipeline:

```
Socket
  ↓
Handlers (security, logging, timeouts)
  ↓
Codecs (HTTP, custom protocol)
  ↓
Business logic
```

---

# 2. Add Dependency

### Maven

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-handler</artifactId>
    <version>4.1.108.Final</version>
</dependency>
```

Usually used together with:

```
netty-transport
netty-buffer
netty-codec
```

---

# 3. Common Handlers in `netty-handler`

Some of the most frequently used handlers include:

| Handler                 | Purpose                 |
| ----------------------- | ----------------------- |
| `SslHandler`            | TLS/SSL encryption      |
| `IdleStateHandler`      | detect idle connections |
| `ReadTimeoutHandler`    | close slow clients      |
| `WriteTimeoutHandler`   | detect blocked writes   |
| `LoggingHandler`        | network logging         |
| `ChunkedWriteHandler`   | streaming large files   |
| `TrafficShapingHandler` | bandwidth throttling    |

These handlers help build **robust and production-ready servers**.

---

# 4. Example: Logging Network Traffic

`LoggingHandler` logs inbound and outbound events.

```java
pipeline.addLast(new LoggingHandler(LogLevel.INFO));
```

Example log:

```
READ: 128B
WRITE: 42B
CHANNEL ACTIVE
```

Useful for debugging network protocols.

---

# 5. Example: Detect Idle Connections

`IdleStateHandler` detects inactive connections.

```java
pipeline.addLast(
    new IdleStateHandler(
        60,  // read idle
        30,  // write idle
        0    // all idle
    )
);
```

You handle idle events in your handler:

```java
@Override
public void userEventTriggered(ChannelHandlerContext ctx, Object evt) {

    if (evt instanceof IdleStateEvent) {
        ctx.close();
    }
}
```

Use cases:

* close dead connections
* implement heartbeats
* detect dropped clients

---

# 6. Example: Enable TLS (SSL)

`SslHandler` enables encrypted connections.

Example TLS setup:

```java
SslContext sslContext = SslContextBuilder
    .forServer(certFile, keyFile)
    .build();
```

Add to pipeline:

```java
pipeline.addLast(sslContext.newHandler(channel.alloc()));
```

Pipeline example:

```
SslHandler
HttpServerCodec
HttpObjectAggregator
BusinessHandler
```

This enables **HTTPS support**.

---

# 7. Example: Read Timeout Protection

Prevent clients from hanging connections forever.

```java
pipeline.addLast(new ReadTimeoutHandler(30));
```

If no data arrives within **30 seconds**, the connection closes.

Good protection against:

* slow clients
* certain DoS attacks

---

# 8. Example: Streaming Large Files

`ChunkedWriteHandler` helps send large streams.

Example:

```java
pipeline.addLast(new ChunkedWriteHandler());
```

Then you can send a file:

```java
ctx.writeAndFlush(new ChunkedFile(file));
```

Used for:

* file servers
* video streaming
* large downloads

---

# 9. Example Pipeline

A realistic Netty server pipeline might look like:

```
SslHandler
LoggingHandler
IdleStateHandler
ReadTimeoutHandler
HttpServerCodec
HttpObjectAggregator
ChunkedWriteHandler
BusinessHandler
```

Responsibilities:

| Layer         | Purpose        |
| ------------- | -------------- |
| Security      | TLS            |
| Observability | logging        |
| Stability     | idle detection |
| Protocol      | HTTP decoding  |
| Application   | business logic |

---

# 10. Traffic Shaping

`TrafficShapingHandler` limits bandwidth usage.

Example:

```java
pipeline.addLast(
    new GlobalTrafficShapingHandler(
        executor,
        1_000_000, // write limit
        1_000_000  // read limit
    )
);
```

Useful for:

* API gateways
* rate limiting
* network throttling

---

# 11. When to Use `netty-handler`

Use this module when building:

| System               | Why                   |
| -------------------- | --------------------- |
| HTTP servers         | TLS, timeouts         |
| API gateways         | traffic shaping       |
| messaging systems    | connection management |
| custom TCP protocols | idle detection        |
| streaming servers    | chunked file writes   |

It adds **production-grade networking capabilities** on top of the core Netty.

---

# 12. Common Pitfalls

### 1️⃣ Wrong handler order

Example mistake:

```
HttpServerCodec
SslHandler
```

Correct:

```
SslHandler
HttpServerCodec
```

Security handlers should come **first**.

---

### 2️⃣ Missing idle detection

Without `IdleStateHandler`, dead connections may stay open forever.

---

### 3️⃣ Excessive logging

`LoggingHandler` is useful for debugging but may cause:

* high I/O
* large logs

Use it carefully in production.

---

# 13. Summary

`netty-handler` provides **high-level reusable networking handlers** that add important capabilities to Netty pipelines.

Key features:

```
TLS/SSL support
Idle connection detection
Timeout handling
Traffic shaping
Logging
File streaming
```

These handlers allow developers to build **secure, stable, and production-ready network servers** using Netty.

---

✅ **In simple terms**

```
Transport → Handlers → Codecs → Business Logic
```

`netty-handler` is the **middleware layer of Netty networking pipelines**.