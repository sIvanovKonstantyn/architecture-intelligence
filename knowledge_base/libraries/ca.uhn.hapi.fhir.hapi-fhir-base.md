The artifact **`ca.uhn.hapi.fhir:hapi-fhir-base`** is the **core foundation module** of the HAPI FHIR framework.
It provides the **low-level infrastructure** used by other HAPI FHIR modules but **does not include actual FHIR resource models** (like Patient, Observation, etc.).

Instead, it contains:

* Core FHIR utilities
* Parsers and encoding infrastructure
* Context initialization (`FhirContext`)
* Interceptors and client/server base interfaces
* Version-independent abstractions

In most projects you **don’t use it directly**, but it is **transitively included** when you add modules like:

* `hapi-fhir-client`
* `hapi-fhir-server`
* `hapi-fhir-structures-r4`
* `hapi-fhir-structures-dstu3`

---

# Quick Guide: Using `hapi-fhir-base`

## 1️⃣ Add dependencies

Example Maven setup for **FHIR R4**:

```xml
<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-base</artifactId>
    <version>7.0.0</version>
</dependency>

<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-structures-r4</artifactId>
    <version>7.0.0</version>
</dependency>
```

Normally you only add the **structures module**, and `hapi-fhir-base` comes automatically.

---

# 2️⃣ Create a `FhirContext`

The **central entry point** of HAPI FHIR is `FhirContext`.

```java
import ca.uhn.fhir.context.FhirContext;

FhirContext ctx = FhirContext.forR4();
```

`FhirContext` is:

* expensive to create
* thread-safe
* should be a **singleton**

Example Spring bean:

```java
@Bean
public FhirContext fhirContext() {
    return FhirContext.forR4();
}
```

---

# 3️⃣ Parse FHIR JSON/XML

The base module provides **FHIR parsers**.

```java
String json = "{ \"resourceType\": \"Patient\", \"id\": \"123\" }";

Patient patient = ctx.newJsonParser()
        .parseResource(Patient.class, json);
```

Serialize back:

```java
String output = ctx.newJsonParser()
        .setPrettyPrint(true)
        .encodeResourceToString(patient);
```

---

# 4️⃣ Work with FHIR resources

Using the model from `hapi-fhir-structures-r4`:

```java
Patient patient = new Patient();
patient.addName()
       .setFamily("Doe")
       .addGiven("John");

patient.setGender(AdministrativeGender.MALE);
```

Serialize:

```java
String json = ctx.newJsonParser().encodeResourceToString(patient);
```

Output:

```json
{
 "resourceType": "Patient",
 "name": [{
   "family": "Doe",
   "given": ["John"]
 }]
}
```

---

# 5️⃣ Create a FHIR REST client

Using HAPI client infrastructure:

```java
IGenericClient client = ctx.newRestfulGenericClient(
    "https://fhir.example.com/fhir"
);

Patient patient = client
        .read()
        .resource(Patient.class)
        .withId("123")
        .execute();
```

---

# 6️⃣ Interceptors

The base module provides **interceptor support**.

Example: logging requests.

```java
client.registerInterceptor(new LoggingInterceptor());
```

Or create your own:

```java
public class MyInterceptor {

    @Hook(Pointcut.CLIENT_REQUEST)
    public void onRequest(IHttpRequest request) {
        System.out.println("Request: " + request.getUri());
    }
}
```

---

# Architecture overview

```
HAPI FHIR
│
├── hapi-fhir-base
│     Core utilities
│     Parsers
│     FhirContext
│
├── hapi-fhir-structures-r4
│     Resource models
│
├── hapi-fhir-client
│     REST client
│
└── hapi-fhir-server
      REST server framework
```

So **`hapi-fhir-base` = framework core**.

---

# Best Practices

### 1️⃣ Reuse `FhirContext`

Bad:

```java
FhirContext.forR4();
```

inside every method.

Good:

```
Singleton / Spring bean
```

---

### 2️⃣ Choose correct FHIR version

```java
FhirContext.forR4();
FhirContext.forR5();
FhirContext.forDstu3();
```

FHIR versions are **not compatible**.

---

### 3️⃣ Prefer JSON over XML

FHIR JSON is:

* faster
* more widely used
* default in most APIs.

---

# Typical Use Cases

You use HAPI FHIR when building:

* **Healthcare APIs**
* **FHIR servers**
* **HL7 integrations**
* **EHR integrations**
* **Medical data pipelines**

Many healthcare platforms use this stack with **Spring Boot + HL7 FHIR.

---
