"""
Simple Test Client for RAG Query API

This script demonstrates how to interact with the asynchronous RAG API:
1. Submit a query
2. Poll for completion
3. Display the result
"""

import requests
import time
import sys


def submit_query(query: str, base_url: str = "http://localhost:8000") -> str:
    """
    Submit a query to the API.
    
    Args:
        query: The question to ask
        base_url: API base URL
        
    Returns:
        str: Job ID for tracking
    """
    print(f"📤 Submitting query: '{query}'")
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            params={"query": query},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        job_id = data["job_id"]
        
        print(f"✅ Query queued successfully!")
        print(f"🆔 Job ID: {job_id}")
        
        return job_id
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API server")
        print("   Make sure the server is running: python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error submitting query: {e}")
        sys.exit(1)


def check_status(job_id: str, base_url: str = "http://localhost:8000") -> dict:
    """
    Check the status of a job.
    
    Args:
        job_id: The job ID to check
        base_url: API base URL
        
    Returns:
        dict: Job status information
    """
    try:
        response = requests.get(
            f"{base_url}/job-status/{job_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        sys.exit(1)


def get_result(job_id: str, base_url: str = "http://localhost:8000") -> str:
    """
    Get the result of a completed job.
    
    Args:
        job_id: The job ID to retrieve
        base_url: API base URL
        
    Returns:
        str: The AI-generated response
    """
    try:
        response = requests.get(
            f"{base_url}/result/{job_id}",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] != "completed":
            return None
            
        return data["result"]
        
    except Exception as e:
        print(f"❌ Error getting result: {e}")
        sys.exit(1)


def wait_for_result(job_id: str, base_url: str = "http://localhost:8000", 
                   max_wait: int = 60, poll_interval: int = 2) -> str:
    """
    Poll for job completion and return result.
    
    Args:
        job_id: The job ID to wait for
        base_url: API base URL
        max_wait: Maximum seconds to wait
        poll_interval: Seconds between polls
        
    Returns:
        str: The AI-generated response
    """
    print(f"\n⏳ Waiting for result (max {max_wait}s)...")
    
    start_time = time.time()
    dots = 0
    
    while time.time() - start_time < max_wait:
        # Check status
        status_data = check_status(job_id, base_url)
        status = status_data["status"]
        
        if status == "finished":
            print("\n✅ Job completed!")
            result = get_result(job_id, base_url)
            return result
            
        elif status == "failed":
            error = status_data.get("error", "Unknown error")
            print(f"\n❌ Job failed: {error}")
            sys.exit(1)
            
        else:
            # Show progress
            dots = (dots + 1) % 4
            print(f"\r   Status: {status}{'.' * dots}   ", end="", flush=True)
            time.sleep(poll_interval)
    
    print(f"\n⏰ Timeout: Job did not complete within {max_wait} seconds")
    print(f"   Job ID: {job_id}")
    print(f"   You can check status later with: GET /job-status/{job_id}")
    sys.exit(1)


def main():
    """
    Main function - interactive test client.
    """
    print("=" * 60)
    print("RAG Query API - Test Client")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Server is running: {response.json()['status']}")
    except:
        print("❌ Server is not running!")
        print("   Start it with: python main.py")
        sys.exit(1)
    
    print()
    
    # Get query from user or use default
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Enter your query (or press Enter for default):")
        query = input("❓ Query: ").strip()
        
        if not query:
            query = "What is this document about?"
            print(f"   Using default: '{query}'")
    
    print()
    
    # Submit query
    job_id = submit_query(query)
    
    # Wait for result
    result = wait_for_result(job_id)
    
    # Display result
    print("\n" + "=" * 60)
    print("🤖 AI Response:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    
    print(f"\n✨ Done! Job ID: {job_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
