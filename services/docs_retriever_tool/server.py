import os, asyncio, json
from fastmcp import FastMCP
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.text_splitter import RecursiveCharacterTextSplitter

VECTOR_DB_URL = os.environ.get("VECTOR_DB_URL", "http://vector_db:6333")
embeddings = OpenAIEmbeddings()
client = QdrantClient(url=VECTOR_DB_URL)

# Create collection if it doesn't exist
try:
    client.get_collection("docs")
except:
    client.create_collection(
        collection_name="docs", vectors_config={"size": 1536, "distance": "Cosine"}
    )

vector_store = QdrantVectorStore(
    client=client,
    collection_name="docs",
    embedding=embeddings,
)

app = FastMCP(name="docs_retriever_tool")


@app.tool(name="retrieve_docs", description="Semantic search over indexed documents.")
async def retrieve(query: str, k: int = 4):
    docs = vector_store.similarity_search(query, k=k)
    return {"passages": [d.page_content for d in docs]}


if __name__ == "__main__":
    asyncio.run(app.run_http_async(host="0.0.0.0", port=7002))
