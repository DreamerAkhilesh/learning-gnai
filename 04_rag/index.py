"""
RAG (Retrieval-Augmented Generation) System - Indexing and Query Script

This script:
1. Loads a PDF document
2. Splits it into smaller chunks
3. Creates embeddings for each chunk
4. Stores embeddings in Qdrant vector database
5. Accepts user queries and retrieves relevant context
6. Uses OpenAI to generate answers based on retrieved context
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# Load environment variables from .env file (for API keys)
load_dotenv()

# Initialize OpenAI client for generating responses
openai_client = OpenAI()

# ============================================================================
# STEP 1: Load PDF Document
# ============================================================================

# Construct path to the PDF file in the same directory as this script
pdf_path = Path(__file__).parent / "LOCAL LINK.pdf"

# Load the PDF document using LangChain's PyPDFLoader
# This extracts text content and metadata from each page
loader = PyPDFLoader(pdf_path)
docs = loader.load()

print(f"Loaded {len(docs)} pages from PDF")

# ============================================================================
# STEP 2: Split Documents into Chunks
# ============================================================================

# Split the documents into smaller chunks for better retrieval
# chunk_size: Maximum characters per chunk (100 is small, consider 500-1000 for production)
# chunk_overlap: Number of characters to overlap between chunks (helps maintain context)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, 
    chunk_overlap=20
)
chunks = text_splitter.split_documents(docs)

print(f"Split into {len(chunks)} chunks")

# ============================================================================
# STEP 3: Create Embeddings
# ============================================================================

# Try to use FastEmbed for local, fast embeddings (no API calls needed)
# Falls back to FakeEmbeddings if FastEmbed is not installed
try:
    from langchain_community.embeddings import FastEmbedEmbeddings
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    print("Using FastEmbed embeddings")
except ImportError:
    # Fallback to fake embeddings for testing (no semantic meaning)
    from langchain_core.embeddings import FakeEmbeddings
    embeddings = FakeEmbeddings(size=384)
    print("⚠️  Using fake embeddings for testing - install fastembed for real embeddings")

# ============================================================================
# STEP 4: Store Embeddings in Qdrant Vector Database
# ============================================================================

# Create vector store from documents
# This will:
# 1. Generate embeddings for each chunk
# 2. Store them in Qdrant at localhost:6333
# 3. Create a collection named "learning_rag"
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)
print("✅ Indexing completed for the document")

# ============================================================================
# STEP 5: Query Interface
# ============================================================================

# Get user query
user_query = input("\n💬 Ask a question about the document: ")

# Perform similarity search to find relevant chunks
# Returns the most similar chunks based on vector similarity
search_results = vector_store.similarity_search(query=user_query)

print(f"\n🔍 Found {len(search_results)} relevant chunks")

# ============================================================================
# STEP 6: Build Context from Search Results
# ============================================================================

# Format the search results into a context string
# Includes page content, page number, and source file location
context = "\n\n---\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page', 'N/A')}\n"
    f"File Location: {result.metadata.get('source', 'N/A')}"
    for result in search_results
])

# ============================================================================
# STEP 7: Generate Response using OpenAI
# ============================================================================

# System prompt that instructs the AI on how to use the context
SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers questions based on the available context extracted from a PDF file.

Instructions:
- Answer questions ONLY based on the provided context
- If the answer is not in the context, say "I don't have enough information to answer that"
- Reference the page number when providing information
- Be concise and accurate

Context:
{context}
"""

# Call OpenAI API to generate response
# Note: Using gpt-4 or gpt-3.5-turbo (gpt-5 doesn't exist yet)
response = openai_client.chat.completions.create(
    model="gpt-4",  # Changed from "gpt-5" which doesn't exist
    messages=[  # Fixed: was "message", should be "messages"
        {"role": "system", "content": SYSTEM_PROMPT},  # Fixed: was "prompt", should be "content"
        {"role": "user", "content": user_query}  # Fixed: was "prompt", should be "content"
    ]
)

# ============================================================================
# STEP 8: Display Response
# ============================================================================

# Print the AI's response
# Fixed: was "Response" (capital R), should be "response" (lowercase)
print(f"\n🤖 Response: {response.choices[0].message.content}")