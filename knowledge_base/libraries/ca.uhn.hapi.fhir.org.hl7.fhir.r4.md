The package **`ca.uhn.hapi.fhir.org.hl7.fhir.r4`** contains the **low-level reference implementation classes for FHIR R4** bundled inside the HAPI FHIR libraries.

It is part of the module:

```
hapi-fhir-structures-r4
```

and contains classes originally from the **FHIR reference model** provided by the HL7 project for the HL7 FHIR R4 specification.

However, **these classes are usually NOT the ones you should use directly** in application code.

There are **two FHIR models in HAPI**:

| Model                    | Package                                  | Typical usage                  |
| ------------------------ | ---------------------------------------- | ------------------------------ |
| HAPI Model (recommended) | `org.hl7.fhir.r4.model`                  | used by most HAPI applications |
| Reference Model          | `ca.uhn.hapi.fhir.org.hl7.fhir.r4.model` | internal / validator / tooling |

---

# Why this package exists

The package is **relocated** under:

```
ca.uhn.hapi.fhir.org.hl7.fhir.r4
```

to avoid dependency conflicts with other FHIR implementations.

It contains:

* validation infrastructure
* terminology support
* canonical FHIR definitions
* advanced tooling classes

This model is heavily used by:

* FHIR validators
* profile processing
* structure definitions
* terminology services

---

# When you should use it

Typical use cases:

* building **FHIR validators**
* working with **StructureDefinition**
* implementing **terminology services**
* building **FHIR tooling**

Most normal integrations **should not use it directly**.

Instead use:

```
org.hl7.fhir.r4.model
```

from `hapi-fhir-structures-r4`.

---

# 1️⃣ Add dependency

```xml
<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-structures-r4</artifactId>
    <version>7.0.0</version>
</dependency>
```

This dependency includes both:

* HAPI resource models
* the reference model (`ca.uhn.hapi.fhir.org.hl7.fhir.r4`)

---

# 2️⃣ Example: using the reference model

Example `Patient` resource from the reference model:

```java
import ca.uhn.hapi.fhir.org.hl7.fhir.r4.model.Patient;

Patient patient = new Patient();
patient.setId("123");
```

But again — normally you should instead use:

```java
import org.hl7.fhir.r4.model.Patient;
```

because it integrates better with the HAPI APIs.

---

# 3️⃣ Typical usage: FHIR validation

The reference model is used by the **FHIR validator**.

Example:

```java
FhirContext ctx = FhirContext.forR4();

FhirValidator validator = ctx.newValidator();

ValidationResult result = validator.validateWithResult(resource);
```

Behind the scenes the validator uses the **reference implementation classes** located in:

```
ca.uhn.hapi.fhir.org.hl7.fhir.r4
```

---

# Architecture overview

```
Application
     │
     ▼
org.hl7.fhir.r4.model
(HAPI resource model)
     │
     ▼
HAPI Infrastructure
     │
     ▼
ca.uhn.hapi.fhir.org.hl7.fhir.r4
(FHIR reference implementation)
```

So the **reference model is a lower-level layer** used internally.

---

# Best Practices

### 1️⃣ Prefer HAPI model classes

Use:

```java
org.hl7.fhir.r4.model.Patient
```

instead of:

```
ca.uhn.hapi.fhir.org.hl7.fhir.r4.model.Patient
```

---

### 2️⃣ Use reference model only for tooling

Examples:

* profile validation
* FHIR schema tooling
* custom validators

---

### 3️⃣ Avoid mixing models

Mixing both models in the same codebase can create:

* conversion overhead
* compatibility issues
* confusing APIs

---

# Quick summary

| Component                          | Purpose                           |
| ---------------------------------- | --------------------------------- |
| `hapi-fhir-base`                   | core framework                    |
| `hapi-fhir-client`                 | REST client                       |
| `hapi-fhir-structures-r4`          | FHIR R4 resource classes          |
| `ca.uhn.hapi.fhir.org.hl7.fhir.r4` | internal reference implementation |

---

✅ **Rule of thumb**

For **95% of projects** using HAPI FHIR with Spring Boot:

Use

```
org.hl7.fhir.r4.model.*
```

and ignore the `ca.uhn.hapi.fhir.org.hl7.fhir.r4` package unless you're building **FHIR tooling or validators**.


