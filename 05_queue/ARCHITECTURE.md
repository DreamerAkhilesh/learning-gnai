# Architecture Documentation - Asynchronous RAG System

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Browser  │  │   cURL   │  │  Python  │  │   Other  │           │
│  │   UI     │  │   CLI    │  │  Script  │  │  Clients │           │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘           │
│        │             │             │             │                  │
│        └─────────────┴─────────────┴─────────────┘                  │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API LAYER                                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Server (server.py)                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │  │
│  │  │   GET    │  │   POST   │  │   GET    │  │   GET    │     │  │
│  │  │    /     │  │  /chat   │  │/job-status│  │ /result  │     │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      QUEUE LAYER                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              Redis Queue (RQ) - client/rq_client.py           │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │                  Valkey (Redis)                          │ │  │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │ │  │
│  │  │  │   Queue    │  │   Jobs     │  │  Results   │        │ │  │
│  │  │  │ rag_queries│  │  Metadata  │  │   Cache    │        │ │  │
│  │  │  └────────────┘  └────────────┘  └────────────┘        │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      WORKER LAYER                                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              RQ Worker (queues/worker.py)                     │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │              process_query(query: str)                   │ │  │
│  │  │  1. Search vector DB                                     │ │  │
│  │  │  2. Build context                                        │ │  │
│  │  │  3. Call OpenAI                                          │ │  │
│  │  │  4. Return result                                        │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    DATA LAYER            │  │   EXTERNAL SERVICES      │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │  Qdrant Vector DB  │  │  │  │   OpenAI API       │  │
│  │  ┌──────────────┐  │  │  │  │  ┌──────────────┐  │  │
│  │  │ Collection:  │  │  │  │  │  │   GPT-4      │  │  │
│  │  │learning_rag  │  │  │  │  │  │   Model      │  │  │
│  │  │              │  │  │  │  │  └──────────────┘  │  │
│  │  │ - Embeddings │  │  │  │  └────────────────────┘  │
│  │  │ - Metadata   │  │  │  └──────────────────────────┘
│  │  │ - Chunks     │  │  │
│  │  └──────────────┘  │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

## Request Flow

### 1. Query Submission Flow

```
Client                FastAPI              Redis Queue           Worker
  │                      │                      │                   │
  │  POST /chat         │                      │                   │
  │  query="..."        │                      │                   │
  ├────────────────────>│                      │                   │
  │                      │                      │                   │
  │                      │  enqueue(job)        │                   │
  │                      ├─────────────────────>│                   │
  │                      │                      │                   │
  │                      │  job_id              │                   │
  │                      │<─────────────────────┤                   │
  │                      │                      │                   │
  │  {job_id: "abc123"} │                      │                   │
  │<────────────────────┤                      │                   │
  │                      │                      │                   │
  │                      │                      │  dequeue(job)     │
  │                      │                      ├──────────────────>│
  │                      │                      │                   │
  │                      │                      │                   │ process_query()
  │                      │                      │                   ├──────────┐
  │                      │                      │                   │          │
  │                      │                      │                   │<─────────┘
  │                      │                      │                   │
  │                      │                      │  store result     │
  │                      │                      │<──────────────────┤
  │                      │                      │                   │
```

### 2. Result Retrieval Flow

```
Client                FastAPI              Redis Queue
  │                      │                      │
  │  GET /result/abc123 │                      │
  ├────────────────────>│                      │
  │                      │                      │
  │                      │  fetch_job(abc123)   │
  │                      ├─────────────────────>│
  │                      │                      │
  │                      │  job + result        │
  │                      │<─────────────────────┤
  │                      │                      │
  │  {result: "..."}    │                      │
  │<────────────────────┤                      │
  │                      │                      │
```

## Component Details

### 1. FastAPI Server (`server.py`)

**Responsibilities**:
- Accept HTTP requests
- Validate input
- Enqueue jobs
- Return job status
- Serve results

**Endpoints**:
```
GET  /              → Health check
POST /chat          → Submit query
GET  /job-status/:id → Check status
GET  /result/:id    → Get result
```

**Dependencies**:
- FastAPI framework
- RQ client
- Worker function reference

### 2. Redis Queue Client (`client/rq_client.py`)

**Responsibilities**:
- Manage Redis connection
- Create queue instance
- Handle connection pooling

**Configuration**:
```python
Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

### 3. Worker (`queues/worker.py`)

**Responsibilities**:
- Process queued jobs
- Search vector database
- Call OpenAI API
- Return results

**Process Flow**:
```
1. Receive query
2. Search Qdrant (similarity_search)
3. Build context from results
4. Create OpenAI prompt
5. Get AI response
6. Return result
```

### 4. Valkey/Redis (`docker-compose.yml`)

**Responsibilities**:
- Store job queue
- Store job metadata
- Cache results
- Manage job lifecycle

**Data Structures**:
```
Queue: rag_queries
  ├── Pending jobs
  ├── Started jobs
  ├── Finished jobs
  └── Failed jobs
```

## Data Flow

### Query Processing Pipeline

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ FastAPI Validation  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Enqueue to Redis    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Worker Picks Up     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Vector DB Search    │
│ (Qdrant)            │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Build Context       │
│ (Format chunks)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ OpenAI API Call     │
│ (GPT-4)             │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Store Result        │
│ (Redis)             │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Client Retrieves    │
└─────────────────────┘
```

## Scaling Strategies

### Horizontal Scaling

```
                    ┌──────────┐
                    │ FastAPI  │
                    │ Server   │
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────┐
                    │  Redis   │
                    │  Queue   │
                    └────┬─────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │ Worker  │     │ Worker  │     │ Worker  │
   │    1    │     │    2    │     │    3    │
   └─────────┘     └─────────┘     └─────────┘
```

### Load Balancing

```
                    ┌──────────┐
                    │   Load   │
                    │ Balancer │
                    └────┬─────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │FastAPI  │     │FastAPI  │     │FastAPI  │
   │Server 1 │     │Server 2 │     │Server 3 │
   └─────────┘     └─────────┘     └─────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                    ┌──────────┐
                    │  Redis   │
                    │  Queue   │
                    └──────────┘
```

## State Management

### Job States

```
┌─────────┐
│ QUEUED  │ ← Job submitted
└────┬────┘
     │
     ▼
┌─────────┐
│ STARTED │ ← Worker picked up
└────┬────┘
     │
     ├──────────┐
     │          │
     ▼          ▼
┌─────────┐  ┌─────────┐
│FINISHED │  │ FAILED  │
└─────────┘  └─────────┘
```

### State Transitions

```
QUEUED → STARTED → FINISHED (success)
                → FAILED   (error)
                → STOPPED  (cancelled)
```

## Error Handling

### Error Flow

```
┌─────────────┐
│   Error     │
│  Occurs     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Catch Exception     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Log Error           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Mark Job as Failed  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Store Error Info    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Return Error to     │
│ Client              │
└─────────────────────┘
```

## Security Layers

### Recommended Security Architecture

```
┌─────────────────────────────────────────┐
│          Security Layer                  │
│  ┌────────────────────────────────────┐ │
│  │  1. API Gateway                    │ │
│  │     - Rate Limiting                │ │
│  │     - Authentication               │ │
│  │     - Request Validation           │ │
│  └────────────────────────────────────┘ │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Application Layer               │
│  ┌────────────────────────────────────┐ │
│  │  2. FastAPI Server                 │ │
│  │     - Input Sanitization           │ │
│  │     - Authorization                │ │
│  │     - CORS                         │ │
│  └────────────────────────────────────┘ │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Data Layer                      │
│  ┌────────────────────────────────────┐ │
│  │  3. Redis/Qdrant                   │ │
│  │     - Network Isolation            │ │
│  │     - Authentication               │ │
│  │     - Encryption at Rest           │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Monitoring Architecture

```
┌─────────────────────────────────────────┐
│          Monitoring Stack                │
│  ┌────────────────────────────────────┐ │
│  │  Metrics (Prometheus)              │ │
│  │  - Request rate                    │ │
│  │  - Error rate                      │ │
│  │  - Queue depth                     │ │
│  │  - Processing time                 │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Logs (ELK Stack)                  │ │
│  │  - Application logs                │ │
│  │  - Access logs                     │ │
│  │  - Error logs                      │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Tracing (Jaeger)                  │ │
│  │  - Request tracing                 │ │
│  │  - Performance profiling           │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Dashboards (Grafana)              │ │
│  │  - Real-time metrics               │ │
│  │  - Alerts                          │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Deployment Architecture

### Development

```
┌──────────────────────────────────┐
│      Local Machine               │
│  ┌────────────────────────────┐  │
│  │  FastAPI (localhost:8000)  │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  RQ Worker (process)       │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  Valkey (Docker)           │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  Qdrant (Docker)           │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

### Production (Kubernetes)

```
┌─────────────────────────────────────────┐
│          Kubernetes Cluster              │
│  ┌────────────────────────────────────┐ │
│  │  Ingress Controller                │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────┴─────────────────────┐ │
│  │  FastAPI Deployment (3 replicas)   │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────┴─────────────────────┐ │
│  │  Redis StatefulSet                 │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────┴─────────────────────┐ │
│  │  Worker Deployment (5 replicas)    │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────┴─────────────────────┐ │
│  │  Qdrant StatefulSet                │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Performance Characteristics

### Latency Breakdown

```
Total Response Time: ~5-10 seconds

┌─────────────────────────────────────┐
│ API Processing      │ ~100ms        │
├─────────────────────────────────────┤
│ Queue Enqueue       │ ~10ms         │
├─────────────────────────────────────┤
│ Worker Pickup       │ ~50ms         │
├─────────────────────────────────────┤
│ Vector Search       │ ~200ms        │
├─────────────────────────────────────┤
│ Context Building    │ ~50ms         │
├─────────────────────────────────────┤
│ OpenAI API Call     │ ~4-8 seconds  │
├─────────────────────────────────────┤
│ Result Storage      │ ~10ms         │
└─────────────────────────────────────┘
```

### Throughput

```
Single Worker:
- ~6-12 queries/minute
- Limited by OpenAI API latency

Multiple Workers (5):
- ~30-60 queries/minute
- Linear scaling up to API limits
```

---

**Last Updated**: 2024-02-18
**Version**: 1.0.0
