The artifact **`ca.uhn.hapi.fhir:hapi-fhir-structures-r4`** provides the **Java model classes for FHIR R4 resources** used by the HAPI FHIR framework.

It implements the **R4 version of the** HL7 FHIR specification.

In simple terms:

* `hapi-fhir-base` → core infrastructure (parsers, context, utilities)
* `hapi-fhir-client` → REST client
* **`hapi-fhir-structures-r4` → Java classes for FHIR resources**

This module contains strongly-typed Java representations of FHIR resources such as:

* `Patient`
* `Observation`
* `Encounter`
* `Condition`
* `Medication`
* `Bundle`
* `Practitioner`

These classes allow you to **create, parse, validate, and manipulate FHIR resources in Java**.

---

# 1️⃣ Add dependency

Example Maven configuration:

```xml
<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-structures-r4</artifactId>
    <version>7.0.0</version>
</dependency>
```

This dependency automatically pulls:

* `hapi-fhir-base`
* common FHIR utilities

---

# 2️⃣ Create `FhirContext` for R4

To work with R4 resources you must initialize the correct context:

```java
FhirContext ctx = FhirContext.forR4();
```

Important:

* expensive to create
* thread-safe
* reuse as singleton

Example in Spring Boot:

```java
@Bean
public FhirContext fhirContext() {
    return FhirContext.forR4();
}
```

---

# 3️⃣ Create a FHIR resource

Example: create a `Patient`.

```java
Patient patient = new Patient();

patient.addIdentifier()
       .setSystem("http://hospital.example.org")
       .setValue("12345");

patient.addName()
       .setFamily("Doe")
       .addGiven("John");

patient.setGender(Enumerations.AdministrativeGender.MALE);
patient.setBirthDate(new Date());
```

The resource is a **Java object representation of a FHIR resource**.

---

# 4️⃣ Serialize to JSON

Using the parser from HAPI:

```java
String json = ctx.newJsonParser()
        .setPrettyPrint(true)
        .encodeResourceToString(patient);
```

Example output:

```json
{
  "resourceType": "Patient",
  "identifier": [{
    "system": "http://hospital.example.org",
    "value": "12345"
  }],
  "name": [{
    "family": "Doe",
    "given": ["John"]
  }],
  "gender": "male"
}
```

---

# 5️⃣ Parse JSON into a resource

Example: converting JSON to Java object.

```java
Patient patient = ctx.newJsonParser()
        .parseResource(Patient.class, json);
```

This is very common when receiving responses from a FHIR API.

---

# 6️⃣ Work with Bundles

FHIR APIs often return **Bundle resources** containing multiple results.

Example:

```java
Bundle bundle = ctx.newJsonParser()
        .parseResource(Bundle.class, jsonResponse);
```

Iterate entries:

```java
for (Bundle.BundleEntryComponent entry : bundle.getEntry()) {
    Resource resource = entry.getResource();
    
    if (resource instanceof Patient) {
        Patient p = (Patient) resource;
        System.out.println(p.getNameFirstRep().getFamily());
    }
}
```

---

# 7️⃣ Create other resources

Example: `Observation`.

```java
Observation observation = new Observation();

observation.setStatus(Observation.ObservationStatus.FINAL);

observation.setValue(
        new Quantity()
            .setValue(98.6)
            .setUnit("F")
);
```

FHIR resources are composed of many reusable components:

* `Identifier`
* `HumanName`
* `CodeableConcept`
* `Quantity`
* `Reference`

---

# 8️⃣ References between resources

FHIR resources reference each other.

Example: `Observation` referencing a `Patient`.

```java
observation.setSubject(
        new Reference("Patient/123")
);
```

---

# Architecture overview

```
Application
     │
     │ uses
     ▼
hapi-fhir-structures-r4
     │
     │ defines
     ▼
FHIR Resource Classes
(Patient, Observation, Bundle...)
     │
     ▼
FHIR JSON / XML
```

---

# When to use `hapi-fhir-structures-r4`

Use this module when you need to:

* model **FHIR R4 resources in Java**
* parse **FHIR JSON/XML**
* interact with FHIR APIs
* build healthcare integrations

It is commonly used together with:

* `hapi-fhir-client`
* `hapi-fhir-server`
* Spring Boot applications integrating healthcare systems.

---

# Best Practices

### 1️⃣ Always match the FHIR version

FHIR versions are incompatible.

Examples:

```
hapi-fhir-structures-r4
hapi-fhir-structures-r5
hapi-fhir-structures-dstu3
```

Use the one supported by your FHIR server.

---

### 2️⃣ Prefer `getFirstRep()` helpers

Example:

```java
patient.getNameFirstRep().getFamily();
```

Instead of manually checking lists.

---

### 3️⃣ Reuse parsers

Avoid creating new parsers frequently in hot paths.
