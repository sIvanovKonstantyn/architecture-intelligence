## Guide: Using `io.netty:netty-codec`

### 1. What is `netty-codec`

`netty-codec` is a core module of the Netty that provides **general-purpose encoders and decoders** used to convert **raw network bytes (`ByteBuf`) into higher-level messages and back**.

In Netty terminology:

* **Decoder** → transforms incoming bytes into objects
* **Encoder** → transforms objects into bytes to send over the network

This module contains reusable building blocks used by other Netty protocol implementations like:

* HTTP (via `netty-codec-http`)
* HTTP/2 (via `netty-codec-http2`)
* WebSocket
* Redis protocol
* DNS

---

# 2. Why `netty-codec` Exists

Networking works with **byte streams**:

```
TCP → byte stream
```

Applications work with **messages**:

```
LoginMessage
ChatMessage
HttpRequest
```

`netty-codec` bridges this gap.

```
Bytes (ByteBuf)
     ↓
Decoder
     ↓
Message Objects
     ↓
Business Logic
     ↓
Encoder
     ↓
Bytes
```

---

# 3. Add Dependency

### Maven

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-codec</artifactId>
    <version>4.1.108.Final</version>
</dependency>
```

Usually used together with:

```
netty-transport
netty-buffer
netty-handler
```

---

# 4. Core Classes

Important classes provided by `netty-codec`:

| Class                          | Purpose                         |
| ------------------------------ | ------------------------------- |
| `ByteToMessageDecoder`         | Converts bytes → objects        |
| `MessageToByteEncoder`         | Converts objects → bytes        |
| `MessageToMessageDecoder`      | Object → object transformation  |
| `MessageToMessageEncoder`      | Object → object transformation  |
| `LengthFieldBasedFrameDecoder` | Splits messages by length field |
| `DelimiterBasedFrameDecoder`   | Splits messages by delimiter    |
| `LineBasedFrameDecoder`        | Splits messages by line         |

These are **the most commonly used Netty codec tools**.

---

# 5. Example: Custom Protocol

Imagine a simple protocol:

```
[length:4 bytes][message bytes]
```

Example message:

```
00000005Hello
```

---

# 6. Implement Decoder

Extend `ByteToMessageDecoder`.

```java
public class MyMessageDecoder extends ByteToMessageDecoder {

    @Override
    protected void decode(ChannelHandlerContext ctx,
                          ByteBuf in,
                          List<Object> out) {

        if (in.readableBytes() < 4) {
            return;
        }

        in.markReaderIndex();

        int length = in.readInt();

        if (in.readableBytes() < length) {
            in.resetReaderIndex();
            return;
        }

        byte[] bytes = new byte[length];
        in.readBytes(bytes);

        String message = new String(bytes);

        out.add(message);
    }
}
```

This converts:

```
ByteBuf → String
```

---

# 7. Implement Encoder

Extend `MessageToByteEncoder`.

```java
public class MyMessageEncoder extends MessageToByteEncoder<String> {

    @Override
    protected void encode(ChannelHandlerContext ctx,
                          String msg,
                          ByteBuf out) {

        byte[] bytes = msg.getBytes();

        out.writeInt(bytes.length);
        out.writeBytes(bytes);
    }
}
```

This converts:

```
String → ByteBuf
```

---

# 8. Add to Netty Pipeline

Example server pipeline:

```java
pipeline.addLast(new MyMessageDecoder());
pipeline.addLast(new MyMessageEncoder());
pipeline.addLast(new BusinessHandler());
```

Flow:

```
Incoming TCP
      ↓
ByteToMessageDecoder
      ↓
Message
      ↓
BusinessHandler
      ↓
MessageToByteEncoder
      ↓
Outgoing TCP
```

---

# 9. Built-in Frame Decoders

`netty-codec` already provides powerful decoders.

### Length-based protocol

```
[length][payload]
```

Use:

```java
pipeline.addLast(
    new LengthFieldBasedFrameDecoder(
        65536,
        0,
        4,
        0,
        4
    )
);
```

Very common in binary protocols.

---

### Delimiter-based protocol

Example:

```
hello\n
world\n
```

Use:

```java
pipeline.addLast(new LineBasedFrameDecoder(1024));
```

Used in:

* text protocols
* CLI servers
* telnet services

---

# 10. Message Transformation

Sometimes you only transform objects.

Example:

```
ByteBuf → Json → DomainObject
```

Use:

```
MessageToMessageDecoder
```

Example:

```java
public class JsonDecoder extends MessageToMessageDecoder<String> {

    @Override
    protected void decode(ChannelHandlerContext ctx,
                          String msg,
                          List<Object> out) {

        MyObject obj = parseJson(msg);
        out.add(obj);
    }
}
```

---

# 11. Typical Netty Pipeline

Example production pipeline:

```
LengthFieldBasedFrameDecoder
MessageDecoder
BusinessHandler
MessageEncoder
```

Or HTTP:

```
HttpServerCodec
HttpObjectAggregator
BusinessHandler
```

---

# 12. When to Use `netty-codec`

Use it when building:

| System                   | Why                    |
| ------------------------ | ---------------------- |
| Custom TCP protocols     | encode/decode messages |
| API gateways             | message transformation |
| messaging systems        | framing protocols      |
| high-performance servers | minimal overhead       |

It is a fundamental part of the Netty networking stack.

---

# 13. Common Pitfalls

### 1️⃣ Not handling partial packets

TCP is a **stream**, not message-based.

Bad assumption:

```
1 packet = 1 message
```

Always check:

```
readableBytes()
```

---

### 2️⃣ Memory leaks

Netty buffers are reference-counted.

Use:

```
ByteToMessageDecoder
MessageToByteEncoder
```

to avoid manual releases.

---

### 3️⃣ Blocking in decoder

Decoders run on the **event loop**.

Never perform:

```
DB calls
disk IO
sleep()
```

---

# 14. Summary

`netty-codec` provides **general encoding and decoding infrastructure** used to transform raw TCP byte streams into application messages.

Core components:

```
ByteToMessageDecoder
MessageToByteEncoder
LengthFieldBasedFrameDecoder
DelimiterBasedFrameDecoder
MessageToMessageDecoder
```

It is the **foundation for all higher-level protocol implementations** in Netty.

---

✅ **In simple terms**

```
TCP Bytes
   ↓
netty-codec
   ↓
Application Messages
```