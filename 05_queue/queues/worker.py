from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_community.embeddings import FastEmbedEmbeddings
from dotenv import load_dotenv
load_dotenv()

openai_client = OpenAI()

embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

vector_store = QdrantVectorStore.from_documents(
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

def process_query(query:str):
    print("Searching chunks:", query)
    search_results = vector_store.similarity_search(query=user_query)

    context = "\n\n---\n\n".join([
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page', 'N/A')}\n"
        f"File Location: {result.metadata.get('source', 'N/A')}"
        for result in search_results
    ])
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
            {"role": "user", "content": query}  # Fixed: was "prompt", should be "content"
        ]
    )

    return response.choices[0].message.content