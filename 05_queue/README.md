# Asynchronous RAG Query System with Redis Queue

This project implements an asynchronous RAG (Retrieval-Augmented Generation) query processing system using Redis Queue (RQ) for job management. It's built on top of the RAG system from `04_rag` but adds scalability and non-blocking query processing.

## Architecture Overview

```
User Request → FastAPI Server → Redis Queue → Worker Process → OpenAI
                     ↓                              ↓
                Job ID Return              Vector DB Search
                     ↓                              ↓
            Poll for Status              Generate Response
                     ↓                              ↓
                Get Result ← ← ← ← ← ← ← ← ← ← Result
```

## Components

### 1. **FastAPI Server** (`server.py`)
- REST API for submitting queries and retrieving results
- Non-blocking: returns immediately with a job ID
- Endpoints:
  - `GET /` - Health check
  - `POST /chat` - Submit a query
  - `GET /job-status/{job_id}` - Check job status
  - `GET /result/{job_id}` - Get completed result

### 2. **Redis Queue Client** (`client/rq_client.py`)
- Manages connection to Valkey (Redis-compatible)
- Creates and manages the job queue
- Handles job submission and retrieval

### 3. **Worker Process** (`queues/worker.py`)
- Processes queries asynchronously
- Searches vector database for relevant chunks
- Generates responses using OpenAI
- Runs as a separate process

### 4. **Valkey (Redis)** (`docker-compose.yml`)
- Message broker for RQ
- Stores job queue and results
- Redis-compatible in-memory data store

## Why Use Queues?

### Problems with Synchronous Processing (04_rag)
1. **Blocking**: User waits for entire RAG pipeline to complete
2. **No Concurrency**: Can only handle one query at a time
3. **Timeout Risk**: Long-running queries may timeout
4. **No Retry**: Failed queries are lost
5. **No Monitoring**: Can't track query progress

### Benefits of Asynchronous Processing (05_queue)
1. ✅ **Non-blocking**: API returns immediately with job ID
2. ✅ **Concurrent**: Multiple queries processed simultaneously
3. ✅ **Scalable**: Add more workers to increase throughput
4. ✅ **Resilient**: Failed jobs can be retried
5. ✅ **Monitorable**: Track job status and progress
6. ✅ **Decoupled**: API server and workers run independently

## Trade-offs Made

### 1. Complexity vs Scalability

**Trade-off**: Added complexity (Redis, workers, job management) for better scalability

**Pros:**
- Can handle high query volumes
- Workers can be scaled independently
- Better resource utilization

**Cons:**
- More moving parts to manage
- Requires Redis/Valkey infrastructure
- More complex deployment

### 2. Immediate Response vs Complete Answer

**Trade-off**: Return job ID immediately instead of waiting for answer

**Pros:**
- API never blocks
- Better user experience for long queries
- Can implement progress updates

**Cons:**
- Requires polling or webhooks
- More complex client implementation
- Two-step process (submit + retrieve)

### 3. Valkey vs Redis

**Trade-off**: Using Valkey (Redis fork) instead of official Redis

**Pros:**
- Fully open source (BSD license)
- Redis-compatible
- Active development
- No licensing concerns

**Cons:**
- Newer project (less mature)
- Smaller community
- Could use Redis directly if preferred

### 4. RQ vs Other Queue Systems

**Trade-off**: Using RQ instead of Celery, Bull, or AWS SQS

**RQ Pros:**
- Simple Python API
- Easy to understand
- Good for small to medium scale
- Minimal configuration

**RQ Cons:**
- Less feature-rich than Celery
- No built-in scheduling
- Redis-only (not multi-broker)

**Alternatives:**
- **Celery**: More features, more complex
- **AWS SQS**: Managed service, cloud-dependent
- **RabbitMQ**: More robust, more overhead

## Project Structure

```
05_queue/
├── client/
│   ├── __init__.py
│   └── rq_client.py          # Redis Queue client setup
├── queues/
│   ├── __init__.py
│   └── worker.py             # Worker function for processing queries
├── .env                      # Environment variables (OPENAI_API_KEY)
├── docker-compose.yml        # Valkey (Redis) container setup
├── main.py                   # Server entry point
├── server.py                 # FastAPI application
└── README.md                 # This file
```

## Prerequisites

1. **Qdrant Vector Database** running on `localhost:6333`
   - Start from `04_rag`: `docker-compose up -d`
   
2. **Indexed Documents** in Qdrant
   - Run `04_rag/index.py` first to populate the vector database

3. **Python Dependencies**
   ```bash
   pip install fastapi uvicorn redis rq langchain-qdrant langchain-community openai python-dotenv
   ```

4. **OpenAI API Key**
   - Add to `.env` file: `OPENAI_API_KEY=your_key_here`

## Setup and Running

### Step 1: Start Valkey (Redis)

```bash
cd 05_queue
docker-compose up -d
```

Verify it's running:
```bash
docker ps
# Should show valkey_queue container
```

### Step 2: Start RQ Worker

Open a terminal and run:
```bash
cd 05_queue
rq worker rag_queries --with-scheduler
```

You should see:
```
Worker rq:worker:... started, version 1.x.x
Listening on rag_queries...
```

### Step 3: Start FastAPI Server

Open another terminal and run:
```bash
cd 05_queue
python main.py
```

Server will start at: `http://localhost:8000`

### Step 4: Test the API

**Option 1: Using the Interactive Docs**
- Visit: `http://localhost:8000/docs`
- Try the `/chat` endpoint

**Option 2: Using curl**

Submit a query:
```bash
curl -X POST "http://localhost:8000/chat?query=What%20is%20this%20document%20about?"
```

Response:
```json
{
  "status": "queued",
  "job_id": "abc123...",
  "message": "Your query has been queued for processing"
}
```

Check status:
```bash
curl "http://localhost:8000/job-status/abc123..."
```

Get result:
```bash
curl "http://localhost:8000/result/abc123..."
```

**Option 3: Using Python**

```python
import requests
import time

# Submit query
response = requests.post(
    "http://localhost:8000/chat",
    params={"query": "What is this document about?"}
)
job_id = response.json()["job_id"]
print(f"Job ID: {job_id}")

# Poll for result
while True:
    status_response = requests.get(f"http://localhost:8000/job-status/{job_id}")
    status = status_response.json()["status"]
    
    if status == "finished":
        result_response = requests.get(f"http://localhost:8000/result/{job_id}")
        print(result_response.json()["result"])
        break
    elif status == "failed":
        print("Job failed!")
        break
    
    print(f"Status: {status}, waiting...")
    time.sleep(1)
```

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "Server is up and running",
  "service": "RAG Query API"
}
```

### `POST /chat`
Submit a query for processing.

**Parameters:**
- `query` (string, required): The user's question

**Response:**
```json
{
  "status": "queued",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Your query has been queued for processing"
}
```

### `GET /job-status/{job_id}`
Check the status of a job.

**Response (Queued):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2024-02-18T10:30:00"
}
```

**Response (Finished):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "finished",
  "created_at": "2024-02-18T10:30:00",
  "ended_at": "2024-02-18T10:30:05",
  "result": "The document is about..."
}
```

**Response (Failed):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "created_at": "2024-02-18T10:30:00",
  "error": "Error details..."
}
```

### `GET /result/{job_id}`
Get the result of a completed job.

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": "The document discusses..."
}
```

## Job Lifecycle

```
1. QUEUED    → Job submitted, waiting for worker
2. STARTED   → Worker picked up the job
3. FINISHED  → Job completed successfully
   OR
   FAILED    → Job encountered an error
```

## Scaling

### Horizontal Scaling (Multiple Workers)

Run multiple worker processes:

```bash
# Terminal 1
rq worker rag_queries

# Terminal 2
rq worker rag_queries

# Terminal 3
rq worker rag_queries
```

Jobs will be distributed across all workers automatically.

### Vertical Scaling (Worker Configuration)

Adjust worker settings:

```bash
# Increase burst mode for faster processing
rq worker rag_queries --burst

# Set custom timeout
rq worker rag_queries --timeout 300

# Process multiple jobs per worker
rq worker rag_queries --worker-class rq.Worker
```

## Monitoring

### RQ Dashboard (Optional)

Install and run RQ Dashboard:

```bash
pip install rq-dashboard
rq-dashboard
```

Visit: `http://localhost:9181`

### Manual Monitoring

Check queue status:
```bash
rq info --url redis://localhost:6379
```

View failed jobs:
```bash
rq info --url redis://localhost:6379 --only-failed
```

## Error Handling

### Common Issues

1. **"Job not found"**
   - Job ID is invalid or expired
   - Jobs are cleaned up after completion (configurable)

2. **"Connection refused to Redis"**
   - Valkey container not running
   - Run: `docker-compose up -d`

3. **"Collection not found in Qdrant"**
   - Vector database not populated
   - Run: `cd ../04_rag && python index.py`

4. **"OpenAI API error"**
   - Invalid or missing API key
   - Check `.env` file

### Retry Failed Jobs

```python
from redis import Redis
from rq import Queue
from rq.registry import FailedJobRegistry

redis_conn = Redis(host='localhost', port=6379)
queue = Queue('rag_queries', connection=redis_conn)
registry = FailedJobRegistry(queue=queue)

# Requeue all failed jobs
for job_id in registry.get_job_ids():
    registry.requeue(job_id)
```

## Production Considerations

### 1. Security
- [ ] Add API authentication (JWT, API keys)
- [ ] Use HTTPS/TLS
- [ ] Secure Redis with password
- [ ] Rate limiting

### 2. Reliability
- [ ] Add job result TTL (time-to-live)
- [ ] Implement retry logic
- [ ] Add dead letter queue
- [ ] Monitor worker health

### 3. Performance
- [ ] Use connection pooling
- [ ] Implement caching for common queries
- [ ] Optimize chunk retrieval (adjust k parameter)
- [ ] Use faster embedding models

### 4. Observability
- [ ] Add structured logging
- [ ] Implement metrics (Prometheus)
- [ ] Set up alerting
- [ ] Track job duration and success rate

## Comparison: 04_rag vs 05_queue

| Feature | 04_rag (Synchronous) | 05_queue (Asynchronous) |
|---------|---------------------|------------------------|
| Response Time | Immediate (blocks) | Immediate (job ID) |
| Concurrency | Single query | Multiple queries |
| Scalability | Limited | Horizontal scaling |
| Complexity | Simple | Moderate |
| Infrastructure | Qdrant only | Qdrant + Redis |
| Monitoring | None | Job tracking |
| Retry | No | Yes |
| Best For | Testing, demos | Production, high load |

## Next Steps

1. **Add Webhooks**: Notify clients when jobs complete
2. **Implement Caching**: Cache common queries
3. **Add Streaming**: Stream responses as they're generated
4. **Priority Queues**: Process urgent queries first
5. **Batch Processing**: Process multiple queries together
6. **Add Authentication**: Secure the API
7. **Deploy**: Containerize and deploy to cloud

## Dependencies

```
fastapi>=0.104.0
uvicorn>=0.24.0
redis>=5.0.0
rq>=1.15.0
langchain-qdrant>=0.1.0
langchain-community>=0.0.10
langchain-core>=0.1.0
openai>=1.0.0
python-dotenv>=1.0.0
```

## License

This is a learning project demonstrating asynchronous RAG query processing with Redis Queue.

## Troubleshooting

### Worker not picking up jobs
- Check worker is running: `rq info`
- Verify queue name matches: `rag_queries`
- Check Redis connection

### Jobs failing silently
- Check worker logs
- Verify Qdrant is running and populated
- Check OpenAI API key is valid

### Slow query processing
- Increase number of workers
- Optimize chunk size in 04_rag
- Use faster embedding model
- Reduce number of retrieved chunks (k parameter)

---

**Built with**: FastAPI, Redis Queue, LangChain, Qdrant, OpenAI
