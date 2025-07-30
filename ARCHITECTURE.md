# RAG Process Flow Diagrams

This document provides detailed flow diagrams for the Enterprise RAG IT Support Assistant system.

## 1. Complete RAG Architecture Flow

```mermaid
graph TB
    subgraph "Data Layer"
        CSV[ServiceNow CSV Data]
        VDB[(ChromaDB Vector Store)]
        EMB[OpenAI Embeddings]
    end
    
    subgraph "Processing Layer"
        PREP[Data Preprocessing]
        META[Metadata Extraction]
        CHUNK[Text Chunking]
        EMBED[Embedding Generation]
    end
    
    subgraph "Application Layer"
        API[FastAPI Server]
        QP[Query Processor]
        RET[Document Retriever]
        CHAIN[RAG Chain]
    end
    
    subgraph "AI Layer"
        LLM[GPT-4o Mini]
        PROMPT[ITIL Prompt Template]
        MEM[Conversation Memory]
    end
    
    subgraph "Interface Layer"
        WEB[Web Interface]
        CURL[API Endpoints]
        RESP[JSON Response]
    end
    
    CSV --> PREP
    PREP --> META
    META --> CHUNK
    CHUNK --> EMBED
    EMBED --> EMB
    EMB --> VDB
    
    WEB --> API
    CURL --> API
    API --> QP
    QP --> RET
    RET --> VDB
    VDB --> CHAIN
    CHAIN --> LLM
    LLM --> PROMPT
    PROMPT --> MEM
    MEM --> RESP
    RESP --> WEB
    RESP --> CURL
```

## 2. Query Processing Sequence

```mermaid
sequenceDiagram
    participant User
    participant WebUI as Web Interface
    participant API as FastAPI
    participant QC as Query Classifier
    participant VS as Vector Store
    participant RAG as RAG Chain
    participant LLM as GPT-4o Mini
    participant MEM as Memory
    
    User->>WebUI: Submit Query
    WebUI->>API: POST /chat
    API->>QC: Analyze Query Type
    
    Note over QC: Pattern Detection:<br/>analytical, temporal,<br/>category, priority, etc.
    
    QC->>QC: Determine k parameter<br/>(20-100 documents)
    QC->>VS: Semantic Search
    VS->>VS: Vector Similarity<br/>Search
    VS->>RAG: Return Top-k Documents
    
    RAG->>MEM: Load Conversation<br/>History
    RAG->>LLM: Generate Response<br/>with Context
    
    Note over LLM: ITIL-Compliant<br/>Response Generation<br/>128k Context Window
    
    LLM->>RAG: Generated Response
    RAG->>API: Formatted Answer
    API->>WebUI: JSON Response<br/>+ Metrics
    WebUI->>User: Display Response<br/>+ Performance Data
```

## 3. Data Processing Pipeline

```mermaid
flowchart LR
    subgraph "Input Stage"
        A[Raw CSV Data]
        B[Incident Records]
    end
    
    subgraph "Preprocessing Stage"
        C[Data Validation]
        D[Date Parsing]
        E[Priority Mapping]
        F[Category Standardization]
    end
    
    subgraph "Enrichment Stage"
        G[Resolution Time Calculation]
        H[Severity Classification]
        I[ITIL Structure Mapping]
        J[Metadata Generation]
    end
    
    subgraph "Text Processing Stage"
        K[Structured Text Creation]
        L[Semantic Chunking]
        M[Embedding Generation]
    end
    
    subgraph "Storage Stage"
        N[Vector Storage]
        O[Metadata Indexing]
        P[Persistence Layer]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
```

## 4. Dynamic Query Classification System

```mermaid
graph TD
    A[User Query] --> B[Query Analyzer]
    B --> C{Pattern Detection}
    
    C -->|pattern, trend, count| D[Analytical Query]
    C -->|between, within, time| E[Temporal Query]
    C -->|similar to, type of| F[Category Query]
    C -->|critical, urgent| G[Priority Query]
    C -->|resolved, duration| H[Resolution Query]
    C -->|team, assigned to| I[Team Query]
    C -->|default| J[Standard Query]
    
    D --> K[k=50 documents]
    E --> L[k=100 documents]
    F --> M[k=25 documents]
    G --> N[k=30 documents]
    H --> O[k=40 documents]
    I --> P[k=30 documents]
    J --> Q[k=20 documents]
    
    K --> R[Retrieve & Process]
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
```

## 5. Response Generation Flow

```mermaid
flowchart TB
    subgraph "Input Processing"
        A[User Query]
        B[Query Classification]
        C[Document Retrieval]
    end
    
    subgraph "Context Building"
        D[Retrieved Documents]
        E[Conversation History]
        F[ITIL Prompt Template]
        G[Combined Context]
    end
    
    subgraph "AI Processing"
        H[GPT-4o Mini]
        I[128k Token Processing]
        J[Response Generation]
    end
    
    subgraph "Post-Processing"
        K[HTML Formatting]
        L[Metrics Calculation]
        M[Response Validation]
    end
    
    subgraph "Output"
        N[Formatted Response]
        O[Performance Metrics]
        P[Cost Tracking]
    end
    
    A --> B
    B --> C
    C --> D
    D --> G
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    M --> O
    M --> P
```

## 6. System Performance Optimization

```mermaid
graph LR
    subgraph "Performance Optimization Layers"
        A[Query Classification] --> A1[Smart k Selection]
        B[Vector Storage] --> B1[ChromaDB Persistence]
        C[Model Selection] --> C1[GPT-4o Mini Cost Optimization]
        D[Context Management] --> D1[128k Token Window]
        E[Caching Strategy] --> E1[Vector Store Persistence]
        F[Response Formatting] --> F1[HTML Table Generation]
    end
    
    A1 --> PERF[Overall Performance]
    B1 --> PERF
    C1 --> PERF
    D1 --> PERF
    E1 --> PERF
    F1 --> PERF
    
    PERF --> METRICS[Performance Metrics:<br/>- Response Time: 15-25s<br/>- Cost: $0.003/query<br/>- Token Efficiency: 15k-17k<br/>- Throughput: 10-20 queries/min]
```

## 7. Enterprise Integration Points

```mermaid
graph TB
    subgraph "External Systems"
        SNOW[ServiceNow]
        ITSM[ITSM Tools]
        MON[Monitoring Systems]
    end
    
    subgraph "RAG System Core"
        API[FastAPI Application]
        VDB[Vector Database]
        AI[AI Processing]
    end
    
    subgraph "Output Channels"
        WEB[Web Interface]
        REST[REST API]
        WEBHOOK[Webhooks]
    end
    
    subgraph "Analytics Layer"
        METRICS[Performance Metrics]
        LOGS[Audit Logs]
        REPORTS[Usage Reports]
    end
    
    SNOW --> API
    ITSM --> API
    MON --> API
    
    API --> VDB
    VDB --> AI
    AI --> WEB
    AI --> REST
    AI --> WEBHOOK
    
    API --> METRICS
    METRICS --> LOGS
    LOGS --> REPORTS
```

## Key Performance Indicators

### Response Quality Metrics
- **ITIL Compliance**: 100% structured responses
- **Accuracy**: High relevance through semantic search
- **Completeness**: Comprehensive incident analysis

### System Performance Metrics
- **Response Time**: 15-25 seconds for complex queries
- **Cost Efficiency**: $0.003 per query (98.5% savings vs GPT-4)
- **Token Utilization**: 15k-17k tokens per analytical query
- **Throughput**: 10-20 queries per minute

### Technical Metrics
- **Context Window**: 128k tokens supported
- **Vector Database**: 100k+ incidents supported
- **Embedding Dimensions**: 1536 (OpenAI text-embedding-ada-002)
- **Memory Persistence**: ChromaDB with automatic persistence

This flow documentation provides a comprehensive view of how the RAG system processes queries from initial input through final response generation, highlighting the sophisticated intelligence built into each stage of the process.
