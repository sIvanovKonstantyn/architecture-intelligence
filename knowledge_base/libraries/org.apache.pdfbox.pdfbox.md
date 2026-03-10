**`org.apache.pdfbox:pdfbox`** is a Java library from the **Apache Software Foundation** that allows you to **create, read, manipulate, and extract content from PDF files**. It is part of the **Apache PDFBox** project.

It is widely used in Java applications for tasks like:

* Extracting text from PDFs
* Creating PDF documents
* Modifying existing PDFs
* Adding images or annotations
* Filling forms
* Digital signing

---

# 1. Add Dependency

### Maven

```xml
<dependency>
    <groupId>org.apache.pdfbox</groupId>
    <artifactId>pdfbox</artifactId>
    <version>2.0.30</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.apache.pdfbox:pdfbox:2.0.30'
```

---

# 2. Loading an Existing PDF

```java
import org.apache.pdfbox.pdmodel.PDDocument;

import java.io.File;

public class LoadPdfExample {

    public static void main(String[] args) throws Exception {

        File file = new File("document.pdf");

        try (PDDocument document = PDDocument.load(file)) {

            System.out.println("Number of pages: " + document.getNumberOfPages());

        }
    }
}
```

Important:

* Always close `PDDocument`
* Use **try-with-resources**

---

# 3. Extract Text from PDF

PDFBox provides `PDFTextStripper`.

```java
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.pdmodel.PDDocument;

import java.io.File;

public class ExtractTextExample {

    public static void main(String[] args) throws Exception {

        try (PDDocument document = PDDocument.load(new File("document.pdf"))) {

            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(document);

            System.out.println(text);
        }
    }
}
```

Useful options:

```java
stripper.setStartPage(1);
stripper.setEndPage(5);
```

---

# 4. Creating a New PDF

```java
import org.apache.pdfbox.pdmodel.*;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.pdmodel.PDPageContentStream;

import java.io.IOException;

public class CreatePdfExample {

    public static void main(String[] args) throws IOException {

        PDDocument document = new PDDocument();
        PDPage page = new PDPage();

        document.addPage(page);

        PDPageContentStream content = new PDPageContentStream(document, page);

        content.beginText();
        content.setFont(PDType1Font.HELVETICA, 12);
        content.newLineAtOffset(100, 700);
        content.showText("Hello PDFBox!");
        content.endText();

        content.close();

        document.save("output.pdf");
        document.close();
    }
}
```

---

# 5. Adding an Image to PDF

```java
import org.apache.pdfbox.pdmodel.graphics.image.PDImageXObject;

PDImageXObject image = PDImageXObject.createFromFile("image.png", document);

content.drawImage(image, 100, 500);
```

Coordinates are measured in **points (1/72 inch)**.

---

# 6. Splitting PDF

```java
import org.apache.pdfbox.multipdf.Splitter;

Splitter splitter = new Splitter();
List<PDDocument> pages = splitter.split(document);
```

Each page becomes a separate document.

---

# 7. Merging PDFs

```java
import org.apache.pdfbox.multipdf.PDFMergerUtility;

PDFMergerUtility merger = new PDFMergerUtility();

merger.addSource("file1.pdf");
merger.addSource("file2.pdf");

merger.setDestinationFileName("merged.pdf");

merger.mergeDocuments(null);
```

---

# 8. Working with Forms (AcroForms)

```java
PDAcroForm form = document.getDocumentCatalog().getAcroForm();

PDField field = form.getField("name");

field.setValue("John Doe");
```

Used for **filling PDF forms programmatically**.

---

# 9. Common Use Cases

PDFBox is commonly used for:

* Document processing pipelines
* Invoice parsing
* Report generation
* OCR pipelines (combined with **Tesseract OCR**)
* Compliance document processing
* Digital signatures

---

# 10. Performance Tips

**1️⃣ Use streaming for large PDFs**

```java
Loader.loadPDF(file);
```

(preferred in recent versions)

**2️⃣ Avoid loading huge PDFs fully in memory**

Use memory settings:

```java
PDDocument.load(file, MemoryUsageSetting.setupTempFileOnly());
```

**3️⃣ Reuse `PDFTextStripper` when processing many documents**

---

# 11. Limitations

PDFBox can struggle with:

* Complex layouts (tables, columns)
* Scanned PDFs (requires OCR)
* Exact text positioning extraction

For table extraction libraries often used together with:

* **Tabula**
* **Apache Tika**

---

✅ **Summary**

`org.apache.pdfbox:pdfbox` is a powerful Java library for:

* reading PDFs
* writing PDFs
* extracting text
* editing documents
* working with forms and images

It is one of the **most widely used open-source PDF libraries in the Java ecosystem**.