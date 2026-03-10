`software.amazon.awssdk.ssm` is the **AWS SDK for Java v2 module** for interacting with **AWS Systems Manager (SSM)**. SSM provides services like **Parameter Store**, **Run Command**, **Session Manager**, and **Automation**, allowing you to securely store configuration, secrets, and manage instances.

Here’s a concise guide on how to use it:

---

## 1. Add Dependency

If you use **Maven**:

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>ssm</artifactId>
    <version>2.26.0</version> <!-- use latest -->
</dependency>
```

For **Gradle**:

```gradle
implementation("software.amazon.awssdk:ssm:2.26.0")
```

---

## 2. Initialize the SSM Client

```java
import software.amazon.awssdk.services.ssm.SsmClient;
import software.amazon.awssdk.regions.Region;

SsmClient ssmClient = SsmClient.builder()
    .region(Region.US_EAST_1) // choose your region
    .build();
```

---

## 3. Working with Parameter Store

### a) Store a Parameter

```java
import software.amazon.awssdk.services.ssm.model.PutParameterRequest;
import software.amazon.awssdk.services.ssm.model.ParameterType;

ssmClient.putParameter(PutParameterRequest.builder()
    .name("/myapp/db-password")
    .value("mySecretPassword")
    .type(ParameterType.SECURE_STRING) // SecureString for secrets
    .overwrite(true)
    .build());
```

### b) Retrieve a Parameter

```java
import software.amazon.awssdk.services.ssm.model.GetParameterRequest;

String dbPassword = ssmClient.getParameter(GetParameterRequest.builder()
        .name("/myapp/db-password")
        .withDecryption(true)
        .build())
    .parameter()
    .value();

System.out.println("DB Password: " + dbPassword);
```

### c) List Parameters

```java
import software.amazon.awssdk.services.ssm.model.DescribeParametersRequest;

ssmClient.describeParameters(DescribeParametersRequest.builder().build())
    .parameters()
    .forEach(p -> System.out.println(p.name() + " - " + p.type()));
```

---

## 4. Run Command on EC2 Instances

```java
import software.amazon.awssdk.services.ssm.model.SendCommandRequest;

ssmClient.sendCommand(SendCommandRequest.builder()
    .targets(t -> t.key("InstanceIds").values("i-1234567890abcdef0"))
    .documentName("AWS-RunShellScript")
    .parameters(Map.of("commands", List.of("echo Hello World")))
    .build());
```

---

## 5. Best Practices

* Use **`SecureString`** for sensitive values.
* Enable **encryption with KMS** for secret parameters.
* Use **`withDecryption(true)`** when reading secrets.
* Close `SsmClient` after use: `ssmClient.close();`.
* Consider **caching parameters** for high-performance applications.

---