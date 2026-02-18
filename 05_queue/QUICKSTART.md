# Quick Start Guide - Asynchronous RAG with Redis Queue

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Docker installed and running
- [ ] Completed `04_rag` setup (Qdrant + indexed documents)
- [ ] OpenAI API key

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
cd 05_queue
pip install -r requirements.txt
```

### 2. Configure Environment (30 seconds)

Edit `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start Valkey/Redis (30 seconds)

```bash
docker-compose up -d
```

Verify:
```bash
docker ps
# Should show: valkey_queue container running
```

### 4. Start Worker (30 seconds)

Open a new terminal:
```bash
cd 05_queue
rq worker rag_queries
```

You should see:
```
Worker rq:worker:hostname.1234 started
Listening on rag_queries...
```

### 5. Start API Server (30 seconds)

Open another terminal:
```bash
cd 05_queue
python main.py
```

You should see:
```
🚀 Starting RAG Query API Server...
📚 API Documentation: http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Test It! (1 minute)

**Option A: Browser**
1. Open: http://localhost:8000/docs
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter a query: "What is this document about?"
5. Click "Execute"
6. Copy the `job_id` from response
7. Use `GET /result/{job_id}` to get the answer

**Option B: Command Line**

```bash
# Submit query
curl -X POST "http://localhost:8000/chat?query=What%20is%20this%20document%20about?"

# Copy the job_id from response, then:
curl "http://localhost:8000/result/YOUR_JOB_ID_HERE"
```

**Option C: Python Script**

Create `test_api.py`:
```python
import requests
import time

# Submit query
response = requests.post(
    "http://localhost:8000/chat",
    params={"query": "What is this document about?"}
)
job_id = response.json()["job_id"]
print(f"Job submitted: {job_id}")

# Wait and get result
time.sleep(3)  # Wait for processing
result = requests.get(f"http://localhost:8000/result/{job_id}")
print(f"Answer: {result.json()['result']}")
```

Run it:
```bash
python test_api.py
```

## What You Should See

### Terminal 1 (Worker):
```
Worker rq:worker:hostname.1234 started
Listening on rag_queries...
🔍 Processing query: What is this document about?
📄 Found 4 relevant chunks
🤖 Generating response with OpenAI...
✅ Response generated: The document discusses...
```

### Terminal 2 (Server):
```
INFO:     127.0.0.1:54321 - "POST /chat?query=..." 200 OK
INFO:     127.0.0.1:54322 - "GET /result/abc123" 200 OK
```

### Browser/API Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": "The document discusses various topics including..."
}
```

## Troubleshooting

### "Connection refused to Redis"
```bash
# Check if Valkey is running
docker ps

# If not, start it
docker-compose up -d
```

### "Collection not found"
```bash
# You need to run 04_rag first to create the collection
cd ../04_rag
python index.py
```

### "OpenAI API error"
```bash
# Check your .env file has the correct API key
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### Worker not processing jobs
```bash
# Make sure worker is running and listening to correct queue
rq worker rag_queries

# Check queue status
rq info --url redis://localhost:6379
```

## Architecture at a Glance

```
┌─────────┐      ┌──────────┐      ┌────────┐      ┌────────┐
│ Client  │─────▶│ FastAPI  │─────▶│ Redis  │─────▶│ Worker │
│         │      │ Server   │      │ Queue  │      │Process │
└─────────┘      └──────────┘      └────────┘      └────────┘
     │                                                    │
     │                                                    ▼
     │                                              ┌──────────┐
     │                                              │ Qdrant   │
     │                                              │ Vector   │
     │                                              │ Database │
     │                                              └──────────┘
     │                                                    │
     │                                                    ▼
     │                                              ┌──────────┐
     │◀─────────────────────────────────────────────│ OpenAI   │
     │                                              │ API      │
     └──────────────────────────────────────────────└──────────┘
```

## Next Steps

1. **Read the full README.md** for detailed documentation
2. **Try multiple concurrent queries** to see async benefits
3. **Scale up** by running multiple workers
4. **Monitor** with RQ Dashboard: `pip install rq-dashboard && rq-dashboard`
5. **Customize** the worker function for your use case

## Common Commands

```bash
# Start everything
docker-compose up -d                    # Start Redis
rq worker rag_queries                   # Start worker (terminal 1)
python main.py                          # Start server (terminal 2)

# Monitor
rq info --url redis://localhost:6379   # Check queue status
docker logs valkey_queue                # Check Redis logs

# Stop everything
docker-compose down                     # Stop Redis
# Ctrl+C in worker terminal
# Ctrl+C in server terminal
```

## Success Checklist

- [ ] Valkey container running (`docker ps`)
- [ ] Worker listening (`rq worker` output shows "Listening...")
- [ ] Server running (http://localhost:8000 accessible)
- [ ] Can submit query via `/chat` endpoint
- [ ] Can retrieve result via `/result/{job_id}` endpoint
- [ ] Worker logs show query processing

## Need Help?

1. Check the full **README.md** for detailed documentation
2. Review **04_rag/README.md** for vector database setup
3. Check worker logs for error messages
4. Verify all services are running with `docker ps` and `rq info`

---

**You're all set!** 🎉 Your asynchronous RAG system is now running.
