"""
Redis Queue Client Configuration

This module sets up the connection to Redis (Valkey) and creates a queue
for processing RAG queries asynchronously.
"""

from redis import Redis
from rq import Queue

# Create Redis connection to Valkey (Redis-compatible)
# Valkey is running in Docker on port 6379
redis_connection = Redis(
    host="localhost",
    port=6379,  # Fixed: should be int, not string
    decode_responses=True  # Automatically decode responses to strings
)

# Create RQ (Redis Queue) instance
# This queue will handle asynchronous job processing
queue = Queue(connection=redis_connection, name="rag_queries")