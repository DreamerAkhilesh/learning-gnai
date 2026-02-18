"""
FastAPI Server for Asynchronous RAG Query Processing

This server provides REST API endpoints for:
1. Submitting queries to the queue
2. Checking job status
3. Retrieving results

The server uses Redis Queue (RQ) to process queries asynchronously,
allowing multiple queries to be handled concurrently without blocking.
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query, HTTPException
from client.rq_client import queue  # Fixed: removed leading dot for direct execution
from queues.worker import process_query  # Fixed: removed leading dot

# Initialize FastAPI application
app = FastAPI(
    title="RAG Query API",
    description="Asynchronous RAG query processing with Redis Queue",
    version="1.0.0"
)


@app.get('/')
def root():
    """
    Health check endpoint.
    
    Returns:
        dict: Server status
    """
    return {"status": "Server is up and running", "service": "RAG Query API"}


@app.post('/chat')
def chat(query: str = Query(..., description="The user's question about the document")):
    """
    Submit a query to the processing queue.
    
    This endpoint:
    1. Accepts a user query
    2. Enqueues it for asynchronous processing
    3. Returns a job ID for tracking
    
    Args:
        query (str): The user's question
        
    Returns:
        dict: Job status and job ID
    """
    if not query or query.strip() == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Enqueue the job for processing
    job = queue.enqueue(process_query, query)
    
    return {
        "status": "queued",
        "job_id": job.id,  # Fixed: was job_id (undefined variable)
        "message": "Your query has been queued for processing"
    }


@app.get('/job-status/{job_id}')
def get_job_status(job_id: str):
    """
    Check the status of a queued job.
    
    Args:
        job_id (str): The job ID returned from /chat endpoint
        
    Returns:
        dict: Job status and result (if completed)
    """
    try:
        # Fetch the job from the queue
        job = queue.fetch_job(job_id=job_id)
        
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Build response based on job status
        response = {
            "job_id": job.id,
            "status": job.get_status(),
            "created_at": job.created_at.isoformat() if job.created_at else None,
        }
        
        # Add result if job is finished
        if job.is_finished:
            response["result"] = job.result
            response["ended_at"] = job.ended_at.isoformat() if job.ended_at else None
        
        # Add error if job failed
        elif job.is_failed:
            response["error"] = str(job.exc_info) if job.exc_info else "Unknown error"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching job: {str(e)}")


@app.get('/result/{job_id}')
def get_result(job_id: str):
    """
    Get the result of a completed job.
    
    Args:
        job_id (str): The job ID returned from /chat endpoint
        
    Returns:
        dict: The AI-generated response
    """
    try:
        job = queue.fetch_job(job_id=job_id)
        
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if not job.is_finished:
            return {
                "status": job.get_status(),
                "message": "Job is not yet completed. Check /job-status for updates."
            }
        
        return {
            "job_id": job.id,
            "status": "completed",
            "result": job.result  # Fixed: was job.return_value() which doesn't exist
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching result: {str(e)}")