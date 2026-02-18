"""
Main Entry Point for RAG Query API Server

This script starts the FastAPI server using Uvicorn.
"""

from server import app
import uvicorn


def main():
    """
    Start the FastAPI server.
    
    Server will be available at:
    - http://localhost:8000
    - API docs at: http://localhost:8000/docs
    - ReDoc at: http://localhost:8000/redoc
    """
    print("🚀 Starting RAG Query API Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()