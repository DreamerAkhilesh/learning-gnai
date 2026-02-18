# Gen AI Learning Projects

A comprehensive collection of Generative AI projects demonstrating various concepts from tokenization to production-ready RAG systems with asynchronous processing.

## 📚 Project Overview

This repository contains hands-on implementations of key GenAI concepts, progressing from fundamentals to advanced production patterns.

```
Gen_AI/
├── 01_Tokenization/          # Text tokenization fundamentals
├── 02_HuggingFace/           # Hugging Face model integration
├── 03_weather_agent/         # AI agent with tool calling
├── 04_rag/                   # RAG system with vector database
└── 05_queue/                 # Asynchronous RAG with Redis Queue
```

## 🚀 Projects

### 1. Tokenization (01_Tokenization)
**Concepts**: Text processing, tokenization, encoding/decoding

Learn the fundamentals of how text is converted into tokens that language models can understand.

**Key Topics**:
- Text tokenization
- Token encoding/decoding
- Vocabulary management
- Subword tokenization

**Technologies**: Python, Transformers

---

### 2. Hugging Face Integration (02_HuggingFace)
**Concepts**: Pre-trained models, model loading, inference

Explore how to use pre-trained models from Hugging Face for various NLP tasks.

**Key Topics**:
- Loading pre-trained models
- Model inference
- Tokenizer usage
- Pipeline API

**Technologies**: Python, Transformers, Hugging Face Hub

---

### 3. Weather Agent (03_weather_agent)
**Concepts**: AI agents, tool calling, function calling, API integration

Build an AI agent that can interact with external APIs and tools to answer questions.

**Key Topics**:
- Function/tool calling
- Agent architecture
- API integration
- Gemini AI integration

**Technologies**: Python, Google Gemini, LangChain

**Files**:
- `main_gemini.py` - Gemini-based weather agent
- `simple_weather.py` - Simple weather API integration

---

### 4. RAG System (04_rag)
**Concepts**: Retrieval-Augmented Generation, vector databases, embeddings

Implement a complete RAG system that can answer questions based on PDF documents.

**Key Topics**:
- Document loading and processing
- Text chunking strategies
- Vector embeddings
- Similarity search
- Context-aware generation

**Technologies**: Python, LangChain, Qdrant, OpenAI

**Architecture**:
```
PDF → Load → Chunk → Embed → Store in Qdrant
                                    ↓
User Query → Embed → Search → Build Context → OpenAI → Answer
```

**Key Files**:
- `index.py` - Document indexing and query processing
- `docker-compose.yml` - Qdrant vector database setup
- `README.md` - Comprehensive documentation

**Trade-offs**:
- Synchronous processing (blocking)
- Simple architecture
- Good for learning and testing
- Limited scalability

📖 **[Full Documentation](04_rag/README.md)**

---

### 5. Asynchronous RAG with Queue (05_queue) ⭐
**Concepts**: Asynchronous processing, job queues, scalability, production patterns

Production-ready RAG system with asynchronous query processing using Redis Queue.

**Key Topics**:
- Asynchronous architecture
- Job queue management
- Horizontal scaling
- Non-blocking APIs
- Worker processes
- Job lifecycle management

**Technologies**: Python, FastAPI, Redis Queue (RQ), Valkey, LangChain, Qdrant, OpenAI

**Architecture**:
```
Client → FastAPI → Redis Queue → Worker → Qdrant + OpenAI
   ↓         ↓          ↓           ↓
Job ID   Return    Store Job    Process    Generate
         Immediately              Query     Response
```

**Key Features**:
- ✅ Non-blocking API (returns immediately)
- ✅ Concurrent query processing
- ✅ Horizontal scalability (multiple workers)
- ✅ Job status tracking
- ✅ Comprehensive error handling
- ✅ Production-ready patterns

**API Endpoints**:
- `GET /` - Health check
- `POST /chat` - Submit query (returns job ID)
- `GET /job-status/{id}` - Check job status
- `GET /result/{id}` - Get completed result

**Key Files**:
- `server.py` - FastAPI application
- `queues/worker.py` - Worker process
- `client/rq_client.py` - Redis Queue client
- `main.py` - Application entry point
- `test_client.py` - Interactive test client
- `docker-compose.yml` - Valkey (Redis) setup

**Documentation**:
- 📖 [README.md](05_queue/README.md) - Complete documentation
- 🚀 [QUICKSTART.md](05_queue/QUICKSTART.md) - 5-minute setup guide
- 🏗️ [ARCHITECTURE.md](05_queue/ARCHITECTURE.md) - System architecture
- 📝 [IMPLEMENTATION_NOTES.md](05_queue/IMPLEMENTATION_NOTES.md) - Dev notes
- 📊 [SUMMARY.md](05_queue/SUMMARY.md) - Project overview
- 📑 [INDEX.md](05_queue/INDEX.md) - Documentation index

**Trade-offs**:
- More complex architecture
- Requires Redis/Valkey infrastructure
- Better scalability and performance
- Production-ready with proper error handling

**Comparison with 04_rag**:

| Feature | 04_rag | 05_queue |
|---------|--------|----------|
| Response | Blocking | Non-blocking |
| Concurrency | Single query | Multiple queries |
| Scalability | Limited | Horizontal |
| Complexity | Simple | Moderate |
| Best For | Learning | Production |

📖 **[Full Documentation](05_queue/README.md)** | 🚀 **[Quick Start](05_queue/QUICKSTART.md)**

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **LangChain** - Framework for LLM applications
- **OpenAI GPT-4** - Language model for generation
- **Google Gemini** - Alternative LLM for agents

### Vector Databases
- **Qdrant** - Vector database for similarity search
- **FastEmbed** - Local embeddings (no API required)

### Queue & Caching
- **Valkey** - Redis-compatible in-memory store
- **Redis Queue (RQ)** - Job queue management

### Web Frameworks
- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server

### Document Processing
- **PyPDF** - PDF document loading
- **RecursiveCharacterTextSplitter** - Text chunking

### Development Tools
- **Docker** - Containerization
- **python-dotenv** - Environment management

## 📋 Prerequisites

### Required
- Python 3.8 or higher
- Docker and Docker Compose
- Git

### API Keys
- OpenAI API key (for GPT-4)
- Google API key (for Gemini, optional)

### Python Packages
See `requirements.txt` for complete list. Key packages:
```bash
pip install langchain-community langchain-qdrant openai google-generativeai fastapi uvicorn redis rq python-dotenv
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Gen_AI
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 4. Choose a Project

**For Learning (Start Here)**:
```bash
cd 01_Tokenization
python main.py
```

**For RAG Basics**:
```bash
cd 04_rag
docker-compose up -d  # Start Qdrant
python index.py       # Index documents and query
```

**For Production Patterns**:
```bash
cd 05_queue
docker-compose up -d           # Start Valkey
rq worker rag_queries          # Terminal 1: Start worker
python main.py                 # Terminal 2: Start API server
python test_client.py          # Terminal 3: Test the API
```

## 📖 Learning Path

### Beginner Path
1. **01_Tokenization** - Understand text processing
2. **02_HuggingFace** - Learn model integration
3. **03_weather_agent** - Build your first agent
4. **04_rag** - Implement RAG system

### Advanced Path
1. Complete Beginner Path
2. **05_queue** - Learn production patterns
3. Experiment with scaling (multiple workers)
4. Customize for your use case

## 🏗️ Architecture Evolution

### Stage 1: Fundamentals (01-03)
```
User Input → Model → Output
```
Simple, synchronous processing for learning.

### Stage 2: RAG System (04)
```
Documents → Vector DB → Retrieval → LLM → Answer
```
Synchronous RAG with vector search.

### Stage 3: Production RAG (05)
```
API → Queue → Worker → Vector DB + LLM → Result
```
Asynchronous, scalable, production-ready.

## 📊 Project Comparison

| Project | Complexity | Scalability | Production Ready | Best For |
|---------|-----------|-------------|------------------|----------|
| 01_Tokenization | ⭐ | N/A | ❌ | Learning basics |
| 02_HuggingFace | ⭐ | N/A | ❌ | Model integration |
| 03_weather_agent | ⭐⭐ | Low | ❌ | Agent patterns |
| 04_rag | ⭐⭐⭐ | Low | ⚠️ | RAG fundamentals |
| 05_queue | ⭐⭐⭐⭐ | High | ✅ | Production use |

## 🔑 Key Concepts Covered

### Tokenization & Processing
- Text tokenization
- Encoding/decoding
- Subword tokenization

### Model Integration
- Pre-trained models
- Model inference
- Pipeline usage

### Agent Patterns
- Tool/function calling
- API integration
- Agent architecture

### RAG (Retrieval-Augmented Generation)
- Document processing
- Vector embeddings
- Similarity search
- Context building
- Generation with context

### Production Patterns
- Asynchronous processing
- Job queues
- Horizontal scaling
- Error handling
- Monitoring
- API design

## 🎯 Use Cases

### 04_rag is Best For:
- Learning RAG concepts
- Quick prototypes
- Single-user applications
- Testing and development

### 05_queue is Best For:
- Production deployments
- Multi-user applications
- High query volumes
- Scalable systems
- Long-running queries

## 🔧 Configuration

### Environment Variables
Create `.env` file in project root:
```env
# Required
OPENAI_API_KEY=sk-...

# Optional
GOOGLE_API_KEY=...
```

### Docker Services
Each project with Docker includes a `docker-compose.yml`:
- **04_rag**: Qdrant vector database (port 6333)
- **05_queue**: Valkey/Redis (port 6379) + Qdrant (port 6333)

## 📚 Documentation

### Project-Specific Docs
- [04_rag/README.md](04_rag/README.md) - RAG system documentation
- [05_queue/README.md](05_queue/README.md) - Async RAG documentation
- [05_queue/QUICKSTART.md](05_queue/QUICKSTART.md) - Quick start guide
- [05_queue/ARCHITECTURE.md](05_queue/ARCHITECTURE.md) - Architecture details

### Code Documentation
All code files include comprehensive inline comments and docstrings.

## 🐛 Troubleshooting

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Connection refused" (Docker)**
```bash
docker-compose up -d
docker ps  # Verify containers are running
```

**"API key error"**
- Check `.env` file exists
- Verify API key is correct
- Ensure `.env` is in the correct directory

**"Collection not found" (Qdrant)**
```bash
cd 04_rag
python index.py  # Create and populate collection
```

### Getting Help
1. Check project-specific README files
2. Review inline code comments
3. Check Docker container logs: `docker logs <container_name>`
4. Verify all services are running: `docker ps`

## 🚀 Deployment

### Development
All projects run locally with Docker for dependencies.

### Production (05_queue)
See [05_queue/README.md](05_queue/README.md) for:
- Security considerations
- Scaling strategies
- Monitoring setup
- Deployment architectures

## 🤝 Contributing

This is a learning repository. Feel free to:
- Experiment with the code
- Add new features
- Improve documentation
- Share your learnings

## 📝 License

This is a learning project for educational purposes.

## 🔗 Resources

### Documentation
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [RQ Docs](https://python-rq.org/)

### Related Topics
- Vector databases and embeddings
- Retrieval-Augmented Generation (RAG)
- Asynchronous processing patterns
- API design and scalability
- Production ML systems

## 📈 Progress Tracking

- [x] Tokenization fundamentals
- [x] Model integration
- [x] Agent patterns
- [x] Basic RAG system
- [x] Production RAG with queues
- [ ] Advanced RAG techniques
- [ ] Multi-modal RAG
- [ ] Fine-tuning models
- [ ] Advanced agent patterns

## 🎓 Learning Outcomes

After completing these projects, you will understand:

1. **Fundamentals**
   - How tokenization works
   - How to use pre-trained models
   - How to build AI agents

2. **RAG Systems**
   - Document processing and chunking
   - Vector embeddings and similarity search
   - Context-aware generation
   - Trade-offs in chunk size and retrieval

3. **Production Patterns**
   - Asynchronous processing
   - Job queue management
   - Horizontal scaling
   - Error handling and monitoring
   - API design for ML systems

4. **Architecture**
   - When to use synchronous vs asynchronous
   - How to scale ML applications
   - Production considerations
   - Trade-offs in system design

## 🌟 Highlights

### Most Comprehensive: 05_queue
- 2000+ lines of documentation
- 6 documentation files
- Production-ready architecture
- Comprehensive error handling
- Test client included

### Best for Learning: 04_rag
- Simple, clear architecture
- Well-commented code
- Easy to understand
- Quick to set up

### Most Practical: 03_weather_agent
- Real-world API integration
- Agent patterns
- Tool calling examples

---

**Ready to start?** Begin with `01_Tokenization` or jump to `05_queue` for production patterns!

**Questions?** Check the project-specific README files for detailed documentation.

**Want to contribute?** Feel free to experiment and share your learnings!
