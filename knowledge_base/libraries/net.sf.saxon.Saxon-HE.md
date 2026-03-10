## What is `net.sf.saxon:Saxon-HE`?

**`Saxon-HE` (Saxon Home Edition)** is an open-source **XSLT, XQuery, and XPath processor for Java**.
It is widely used for **transforming XML documents**, validating them, or querying them using XPath/XQuery.

It is maintained by **Saxonica**.

Key characteristics:

* Written in **Java**
* Implements **XSLT 3.0**, **XPath 3.1**, and **XQuery 3.1**
* Works with **JAXP** APIs
* Open-source (Mozilla Public License)
* Optimized XML processing engine

### Saxon editions

| Edition      | Description                                    |
| ------------ | ---------------------------------------------- |
| **Saxon-HE** | Free, open-source version                      |
| **Saxon-PE** | Professional edition                           |
| **Saxon-EE** | Enterprise edition with advanced optimizations |

Most Java applications use **Saxon-HE** for **XML → XML/HTML/JSON transformations**.

---

# Adding Saxon-HE to a Java Project

### Maven

```xml
<dependency>
    <groupId>net.sf.saxon</groupId>
    <artifactId>Saxon-HE</artifactId>
    <version>12.4</version>
</dependency>
```

### Gradle

```gradle
implementation 'net.sf.saxon:Saxon-HE:12.4'
```

---

# Basic Concepts

Saxon processes XML using three main technologies:

| Technology | Purpose                   |
| ---------- | ------------------------- |
| **XPath**  | Query XML nodes           |
| **XSLT**   | Transform XML documents   |
| **XQuery** | Query XML like a database |

The most common usage in Java is **XSLT transformation**.

---

# Example 1 — Transform XML with XSLT

### Example XML

```xml
<users>
    <user>
        <name>Alice</name>
    </user>
</users>
```

### XSLT

```xml
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
    <html>
        <body>
            <h2>User List</h2>
            <ul>
                <xsl:for-each select="users/user">
                    <li><xsl:value-of select="name"/></li>
                </xsl:for-each>
            </ul>
        </body>
    </html>
</xsl:template>

</xsl:stylesheet>
```

---

### Java Code

```java
import net.sf.saxon.TransformerFactoryImpl;

import javax.xml.transform.*;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import java.io.File;

public class SaxonExample {

    public static void main(String[] args) throws Exception {

        TransformerFactory factory = new TransformerFactoryImpl();

        Source xslt = new StreamSource(new File("transform.xsl"));
        Source xml = new StreamSource(new File("users.xml"));

        Transformer transformer = factory.newTransformer(xslt);

        transformer.transform(xml, new StreamResult(System.out));
    }
}
```

Output:

```html
<html>
  <body>
    <h2>User List</h2>
    <ul>
      <li>Alice</li>
    </ul>
  </body>
</html>
```

---

# Example 2 — Using XPath with Saxon

Saxon also provides a **high-performance XPath engine**.

```java
import net.sf.saxon.s9api.*;

public class XPathExample {

    public static void main(String[] args) throws SaxonApiException {

        Processor processor = new Processor(false);
        DocumentBuilder builder = processor.newDocumentBuilder();

        XdmNode document = builder.build(new java.io.File("users.xml"));

        XPathCompiler xpath = processor.newXPathCompiler();
        XPathSelector selector = xpath.compile("//user/name").load();

        selector.setContextItem(document);

        for (XdmItem item : selector) {
            System.out.println(item.getStringValue());
        }
    }
}
```

Output:

```
Alice
```

---

# Example 3 — Modern API (`s9api`)

Saxon recommends using **s9api** instead of JAXP.

Advantages:

* better performance
* full XSLT 3.0 support
* easier API

Example:

```java
Processor processor = new Processor(false);

XsltCompiler compiler = processor.newXsltCompiler();
XsltExecutable executable = compiler.compile(new StreamSource(new File("transform.xsl")));

XsltTransformer transformer = executable.load();

transformer.setSource(new StreamSource(new File("users.xml")));
transformer.setDestination(processor.newSerializer(System.out));

transformer.transform();
```

---

# Typical Use Cases

Saxon is commonly used for:

### 1. XML → HTML transformation

Example:

```
DocBook → HTML
DITA → HTML
FHIR → JSON
```

### 2. XML pipelines

Processing multiple transformations.

### 3. Healthcare systems

Standards like **HL7 FHIR** or CDA often rely on XSLT transformations.

### 4. Data integration

Transform XML into:

* JSON
* CSV
* HTML
* other XML schemas

---

# Performance Tips

1. **Reuse compiled stylesheets**

```java
XsltExecutable executable = compiler.compile(xslt);
```

Compile once, reuse many times.

---

2. **Use streaming when possible**

Large XML files can be processed with streaming mode.

---

3. **Prefer s9api**

Better performance than plain JAXP.

---

# When to Use Saxon

Use Saxon when you need:

* advanced **XSLT 2.0 / 3.0 features**
* **fast XPath queries**
* heavy **XML transformations**
* **standards-compliant XML processing**

The default Java processor (Xalan) only supports **XSLT 1.0**, while Saxon supports **modern XML standards**.

---

✅ **In short**

`Saxon-HE` is the **most widely used Java library for modern XML transformations**, especially when you need **XSLT 2.0/3.0 or powerful XPath queries**.