# Architecture Diagram

```mermaid
flowchart LR
    U[Professional user] --> UI[ProofPilot web intake]
    UI --> API[FastAPI API]
    API --> D[Transparent local demo workflow]
    API -->|AWS mode only| S[Strands Agent]
    S --> T[Evidence ledger tool]
    S --> B[Amazon Bedrock via AWS credentials]
    T --> A[Scope, risks, milestones, questions]
    D --> A
    A --> G{Human approval gate}
    G -->|approved| H[Human sends or commits externally]
    G -->|not approved| R[Draft remains internal]
```

The local demo branch is deliberately non-AI and non-AWS. The AWS branch is a
real Strands invocation path and returns an error instead of fabricating a
model result when AWS is not configured.
