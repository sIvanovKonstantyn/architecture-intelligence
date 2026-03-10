**`org.apache.commons:commons-compress`** is a Java library from the Apache Software Foundation that provides APIs for **working with archive formats and compression algorithms**. It supports reading and writing many formats such as **ZIP, TAR, GZIP, BZIP2, XZ, 7z, AR, and others**.

It is often used when you need to **compress files, extract archives, or process archive streams** in Java applications.

---

# 1. Dependency

### Maven

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-compress</artifactId>
    <version>1.26.1</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.apache.commons:commons-compress:1.26.1'
```

---

# 2. Main Concepts

The library provides two main abstractions:

| Category    | Classes                                           |
| ----------- | ------------------------------------------------- |
| Compression | `CompressorInputStream`, `CompressorOutputStream` |
| Archive     | `ArchiveInputStream`, `ArchiveOutputStream`       |

**Difference**

* **Compression** → compresses a single stream (gzip, bzip2)
* **Archive** → container with multiple files (zip, tar)

Examples:

| Format | Type                  |
| ------ | --------------------- |
| gzip   | compression           |
| bzip2  | compression           |
| tar    | archive               |
| zip    | archive + compression |

---

# 3. Reading a ZIP Archive

```java
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveInputStream;

import java.io.*;

public class ZipReader {

    public static void main(String[] args) throws Exception {

        try (ZipArchiveInputStream zip =
                 new ZipArchiveInputStream(new FileInputStream("archive.zip"))) {

            ZipArchiveEntry entry;

            while ((entry = zip.getNextZipEntry()) != null) {

                System.out.println("File: " + entry.getName());

                ByteArrayOutputStream out = new ByteArrayOutputStream();
                zip.transferTo(out);

                byte[] data = out.toByteArray();
            }
        }
    }
}
```

---

# 4. Creating a ZIP Archive

```java
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream;

import java.io.*;

public class ZipWriter {

    public static void main(String[] args) throws Exception {

        try (ZipArchiveOutputStream zip =
                 new ZipArchiveOutputStream(new FileOutputStream("archive.zip"))) {

            File file = new File("file.txt");

            ZipArchiveEntry entry = new ZipArchiveEntry(file.getName());
            zip.putArchiveEntry(entry);

            try (FileInputStream in = new FileInputStream(file)) {
                in.transferTo(zip);
            }

            zip.closeArchiveEntry();
        }
    }
}
```

---

# 5. Working with TAR + GZIP (tar.gz)

Very common in Linux distributions.

### Extract `tar.gz`

```java
import org.apache.commons.compress.archivers.tar.*;
import org.apache.commons.compress.compressors.gzip.*;

import java.io.*;

public class TarGzExtractor {

    public static void main(String[] args) throws Exception {

        try (GzipCompressorInputStream gzip =
                 new GzipCompressorInputStream(new FileInputStream("archive.tar.gz"));
             TarArchiveInputStream tar =
                 new TarArchiveInputStream(gzip)) {

            TarArchiveEntry entry;

            while ((entry = tar.getNextTarEntry()) != null) {
                System.out.println("Extracting: " + entry.getName());
            }
        }
    }
}
```

---

# 6. Automatic Format Detection

You can detect the compression format automatically.

```java
import org.apache.commons.compress.compressors.*;

InputStream input = new FileInputStream("file.gz");

CompressorInputStream compressor =
        new CompressorStreamFactory().createCompressorInputStream(input);
```

Supported formats include:

* gzip
* bzip2
* xz
* lzma
* zstd
* deflate

---

# 7. Working with 7z Archives

`commons-compress` also supports **7z**, but with a different API.

```java
import org.apache.commons.compress.archivers.sevenz.*;

File file = new File("archive.7z");

try (SevenZFile sevenZFile = new SevenZFile(file)) {

    SevenZArchiveEntry entry;

    while ((entry = sevenZFile.getNextEntry()) != null) {
        System.out.println(entry.getName());
    }
}
```

---

# 8. Typical Use Cases

Developers typically use **commons-compress** for:

* unpacking application distributions (`tar.gz`)
* processing uploaded archives
* backup tools
* CI/CD artifact processing
* log compression
* reading Linux packages

---

# 9. When to Use It vs Standard Java

Java standard library only supports:

* `java.util.zip` → ZIP + GZIP

Use **commons-compress** when you need:

| Feature | Java standard | commons-compress |
| ------- | ------------- | ---------------- |
| ZIP     | ✅             | ✅                |
| GZIP    | ✅             | ✅                |
| TAR     | ❌             | ✅                |
| BZIP2   | ❌             | ✅                |
| XZ      | ❌             | ✅                |
| 7z      | ❌             | ✅                |

---

# 10. Best Practices

* Always use **streaming** APIs (avoid loading archives fully in memory)
* Validate entry paths to prevent **Zip Slip attacks**
* Use `ArchiveStreamFactory` for dynamic format detection

Example safe extraction:

```java
Path target = Paths.get("output").resolve(entry.getName()).normalize();

if (!target.startsWith("output")) {
    throw new SecurityException("Zip Slip detected");
}
```

---

✅ **Summary**

`commons-compress` is the **de-facto Java library for working with archives and compression formats beyond ZIP/GZIP**. It provides a streaming API that allows efficient processing of large archives.