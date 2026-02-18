# RAG System Implementation

This directory contains a Retrieval-Augmented Generation (RAG) system built with LangChain and Qdrant vector database.

## Architecture Overview

- **Document Loader**: PyPDFLoader for processing PDF documents
- **Text Splitting**: RecursiveCharacterTextSplitter for chunking documents
- **Vector Database**: Qdrant (containerized with Docker)
- **Embeddings**: FastEmbed with fallback to FakeEmbeddings
- **Vector Store**: QdrantVectorStore for similarity search

## Files

- `index.py` - Main indexing script that processes documents and stores embeddings
- `docker-compose.yml` - Qdrant vector database setup
- `LOCAL LINK.pdf` - Source document for indexing
- `README.md` - This documentation

## Trade-offs Made During Development

### 1. Embedding Model Selection

**Evolution:**
- Started with OpenAI embeddings → Google embeddings → FastEmbed/FakeEmbeddings

**Trade-offs:**
- **OpenAI**: High quality but requires API key and costs money
- **Google**: Good quality but hit quota limits on free tier
- **FastEmbed**: Local, fast, no API costs but requires additional package
- **FakeEmbeddings**: No dependencies, instant setup but no semantic meaning

**Current Choice**: FastEmbed with FakeEmbeddings fallback
- ✅ No API costs or quota limits
- ✅ Works offline
- ✅ Easy to test and develop
- ❌ Requires additional installation for real embeddings
- ❌ FakeEmbeddings don't provide semantic search

### 2. Text Chunking Strategy

**Current Settings:**
- `chunk_size=100` - Very small chunks
- `chunk_overlap=20` - 20% overlap

**Trade-offs:**
- ✅ Small chunks = more precise retrieval
- ✅ Good for testing with small documents
- ❌ May break semantic coherence
- ❌ More chunks = more storage and processing
- ❌ Might miss broader context

**Recommendation**: Increase to 500-1000 characters for production

### 3. Vector Database Choice

**Qdrant Selection:**
- ✅ Open source and self-hostable
- ✅ Good performance for small to medium datasets
- ✅ Easy Docker setup
- ✅ Good LangChain integration
- ❌ Requires Docker/containerization
- ❌ Additional infrastructure to manage

**Alternative Considered**: In-memory vector stores
- Would be simpler but not persistent

### 4. Development vs Production Considerations

**Current Setup (Development-focused):**
- Local Docker container
- Small chunk sizes for testing
- Fallback embeddings for easy setup
- No authentication or security

**Production Needs:**
- Persistent storage volumes
- Proper embedding model
- Authentication and security
- Monitoring and logging
- Backup strategies

## Getting Started

1. **Start Qdrant:**
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies (optional for real embeddings):**
   ```bash
   pip install fastembed
   ```

3. **Run indexing:**
   ```bash
   python index.py
   ```

## Next Steps

1. **Implement query interface** - Add search/retrieval functionality
2. **Add LLM integration** - Connect to language model for generation
3. **Improve chunking** - Experiment with larger, more semantic chunks
4. **Add real embeddings** - Install FastEmbed for semantic search
5. **Production hardening** - Add error handling, logging, monitoring

## Known Issues

- Currently uses FakeEmbeddings if FastEmbed not installed
- Very small chunk size may not be optimal
- No query interface implemented yet
- Missing error handling for file operations

## Dependencies

- langchain-community
- langchain-text-splitters
- langchain-qdrant
- python-dotenv
- pypdf
- fastembed (optional, for real embeddings)