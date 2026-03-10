The artifact ca.uhn.hapi.fhir:hapi-fhir-client is the REST client module of the HAPI FHIR framework.

It allows Java applications to communicate with FHIR servers using the HL7 FHIR REST API.

Typical operations you can perform:

Read resources (GET /Patient/123)

Create resources (POST /Patient)

Update resources (PUT /Patient/123)

Search (GET /Patient?name=John)

Delete resources

Execute FHIR operations ($validate, $everything, etc.)

It provides a typesafe fluent API instead of manually writing HTTP requests.

1️⃣ Add dependency

Example Maven configuration:

<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-client</artifactId>
    <version>7.0.0</version>
</dependency>

<dependency>
    <groupId>ca.uhn.hapi.fhir</groupId>
    <artifactId>hapi-fhir-structures-r4</artifactId>
    <version>7.0.0</version>
</dependency>

Usually hapi-fhir-base is pulled transitively.

2️⃣ Create FhirContext

The entry point of the client is FhirContext.

FhirContext ctx = FhirContext.forR4();

Important:

expensive to create

thread-safe

should be reused

In Spring Boot:

@Bean
public FhirContext fhirContext() {
    return FhirContext.forR4();
}
3️⃣ Create FHIR REST client
IGenericClient client = ctx.newRestfulGenericClient(
    "https://fhir-server.example.com/fhir"
);

This client automatically:

builds HTTP requests

serializes resources

parses responses

4️⃣ Read resource

Example: fetch a Patient.

Patient patient = client
        .read()
        .resource(Patient.class)
        .withId("123")
        .execute();

Equivalent REST call:

GET /Patient/123
5️⃣ Create resource
Patient patient = new Patient();
patient.addName()
       .setFamily("Doe")
       .addGiven("John");

MethodOutcome outcome = client
        .create()
        .resource(patient)
        .execute();

Equivalent REST:

POST /Patient
6️⃣ Update resource
patient.setId("123");

MethodOutcome outcome = client
        .update()
        .resource(patient)
        .execute();

Equivalent REST:

PUT /Patient/123
7️⃣ Search resources

FHIR searches are very common.

Example: find patients by family name.

Bundle bundle = client
        .search()
        .forResource(Patient.class)
        .where(Patient.FAMILY.matches().value("Doe"))
        .returnBundle(Bundle.class)
        .execute();

Equivalent REST:

GET /Patient?family=Doe

Iterate results:

for (Bundle.BundleEntryComponent entry : bundle.getEntry()) {
    Patient p = (Patient) entry.getResource();
}
8️⃣ Delete resource
client
    .delete()
    .resourceById("Patient", "123")
    .execute();
9️⃣ Pagination

FHIR search results are paginated.

Bundle nextPage = client.loadPage()
        .next(bundle)
        .execute();
🔟 Interceptors (very useful)

You can attach cross-cutting logic such as:

logging

auth headers

metrics

retries

Example logging interceptor:

client.registerInterceptor(new LoggingInterceptor());

Custom interceptor example:

public class AuthInterceptor {

    @Hook(Pointcut.CLIENT_REQUEST)
    public void onRequest(IHttpRequest request) {
        request.addHeader("Authorization", "Bearer token");
    }
}

Register:

client.registerInterceptor(new AuthInterceptor());
Architecture overview
Application
     │
     │
hapi-fhir-client
     │
     │ uses
     ▼
hapi-fhir-base
     │
     ▼
FHIR Server

The client handles:

HTTP

JSON/XML parsing

FHIR semantics

Best Practices
Reuse IGenericClient

Creating new clients repeatedly is expensive.

Prefer:

@Bean
public IGenericClient fhirClient(FhirContext ctx) {
    return ctx.newRestfulGenericClient(baseUrl);
}
Use interceptors for auth

Instead of manually adding headers everywhere.

Use search constants

Instead of raw strings:

Patient.FAMILY.matches().value("Doe")

instead of

?name=Doe

This gives compile-time safety.

Typical real-world use cases

Using hapi-fhir-client to:

integrate with EHR systems

connect to FHIR servers

build healthcare data pipelines

synchronize medical records

Commonly used with:

Spring Boot

HAPI FHIR JPA Server

hospital systems implementing HL7 FHIR.