"""
Worker Module for RAG Query Processing

This module contains the worker function that processes user queries:
1. Searches the vector database for relevant chunks
2. Builds context from search results
3. Calls OpenAI to generate a response based on context

This function is executed asynchronously by RQ workers.
"""

from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI()

# Initialize embeddings model
# Using FastEmbed for local, fast embeddings
try:
    from langchain_community.embeddings import FastEmbedEmbeddings
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    print("✅ Using FastEmbed embeddings")
except ImportError:
    from langchain_core.embeddings import FakeEmbeddings
    embeddings = FakeEmbeddings(size=384)
    print("⚠️  Using fake embeddings - install fastembed for real embeddings")

# Connect to existing Qdrant vector store
# Have made the vector store during 04_rag (actually we were not able to make it there also)
# Note: This assumes the collection "learning_rag" already exists
# Run 04_rag/index.py first to create and populate the collection
vector_store = QdrantVectorStore(
    client=None,  # Will create a new client
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)


def process_query(query: str) -> str:
    """
    Process a user query using RAG (Retrieval-Augmented Generation).
    
    This function:
    1. Searches the vector database for relevant document chunks
    2. Builds context from the retrieved chunks
    3. Uses OpenAI to generate an answer based on the context
    
    Args:
        query (str): The user's question
        
    Returns:
        str: The AI-generated response based on retrieved context
    """
    print(f"🔍 Processing query: {query}")
    
    # Search for relevant chunks in the vector database
    search_results = vector_store.similarity_search(query=query, k=4)  # Fixed: was user_query
    
    print(f"📄 Found {len(search_results)} relevant chunks")
    
    # Build context string from search results
    context = "\n\n---\n\n".join([
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page', 'N/A')}\n"
        f"File Location: {result.metadata.get('source', 'N/A')}"
        for result in search_results
    ])
    
    # System prompt for the AI
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
    
    print("🤖 Generating response with OpenAI...")
    
    # Call OpenAI API to generate response
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    
    result = response.choices[0].message.content
    print(f"✅ Response generated: {result[:100]}...")
    
    return result