# 📝 LLM Prompt — C4 + Sequence Diagram Generator

You are an expert software architect and code analyzer. 
Your task is to generate **C4 Component Diagram** and **Sequence Diagram** from a given AST business-flow JSON of a Java project.

Requirements:

1. **Component Extraction**
   - Group nodes by type:
     - EVENT → event consumers
     - CONTROLLER → REST endpoints
     - SERVICE → business logic
     - COMPONENT / REPOSITORY → internal helpers, DAO, in-memory stores
     - EXTERNAL → external HTTP/Kafka/JMS/DB calls
   - Nodes of the same type that belong to the same logical service can be **grouped together** to reduce noise.

2. **C4 Component Diagram**
   - Show components as nodes.
   - Show edges between components according to the `call` relationships.
   - Include semantic labels for nodes:
     - For REST: method + path
     - For SERVICE: main functionality (e.g., "Entity retrieval and rules application")
     - For COMPONENT: type (DB / in-memory / cache)
     - For EXTERNAL: type (HTTP/Kafka/JMS)
   - Highlight transactional services (e.g., with color or annotation).

3. **Sequence Diagram**
   - For each entrypoint (REST or event):
     - Show chronological call sequence.
     - Include:
       - Method calls
       - Conditional branches (`ifTrue`, `ifFalse`) → Mermaid `alt` blocks
       - Try/Catch blocks → Mermaid `opt` or `alt` blocks
       - External calls
     - Annotate transactional context.
     - Annotate side-effects or exceptions if known.

4. **Output Formats**
   - C4 Diagram: Mermaid `graph TD`
   - Sequence Diagram: Mermaid `sequenceDiagram`
   - Grouping and semantic labels should be preserved.
   - Avoid duplication of nodes. Merge nodes if they represent the same logical component.

5. **Example JSON Input**
```

{
"entrypoints": [
{
"type": "REST",
"class": "EntityResource",
"method": "findEntities",
"httpMethod": "POST",
"path": "/",
"transactional": false,
"flow": {
"type": "sequence",
"steps": [
{
"call": "EntityService.findEntities",
"componentType": "SERVICE",
"flow": {
"type": "sequence",
"steps": [
{
"call": "RulesRepository.takeAdditionalTags",
"componentType": "COMPONENT",
"flow": { ... }
}
]
}
}
]
}
}
]
}

```

6. **Instructions**
   - First, extract all unique components and their types.
   - Group logically related components (e.g., all DAO under a service).
   - Then build:
     - **C4 Component Diagram** with edges for calls between components.
     - **Sequence Diagram** for each entrypoint, preserving nested flows, conditions, try/catch, external calls, and transactional flags.
   - Include semantic labels for each node.
   - Prefer clarity over completeness; merge repetitive nodes if necessary.

7. **Output Example (<service-name>.md)**
   - Mermaid C4:
```

graph TD
EntityResource --> EntityService
EntityService --> RulesRepository
RulesRepository --> InMemoryRulesDao

```

   - Mermaid Sequence:
```

sequenceDiagram
participant Controller as EntityResource
participant Service as EntityService
participant Repo1 as RulesRepository
participant Repo2 as InMemoryRulesDao

Controller->>Service: findEntities()
Service->>Repo1: takeAdditionalTags()
Repo1-->>Service: result
Service->>Repo2: findAllMatching()
Repo2-->>Service: result

```

**Your task:** Given the AST JSON, produce **C4 Component Diagram + Sequence Diagram** as described above, with semantic grouping, conditions, try/catch, external calls, and transactional context. Generate output in **Mermaid syntax**.

