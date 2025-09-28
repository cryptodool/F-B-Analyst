import chromadb
from .config import settings

# Connect to Chroma Cloud over HTTPS
chroma_client = chromadb.HttpClient(
    host="api.trychroma.com",
    port=443,
    ssl=True,
    headers={
        "X-Chroma-API-Key": settings.CHROMA_API_KEY,
        "X-Chroma-Tenant": settings.CHROMA_TENANT,
        "X-Chroma-Database": settings.CHROMA_DATABASE,
    }
)

collection = chroma_client.get_or_create_collection("documents")

def upsert_embedding(doc_id: str, text_chunks: list[str], metadata: dict):
    if not text_chunks:
        return
    ids = [f"{doc_id}_{i}" for i in range(len(text_chunks))]
    collection.upsert(ids=ids, documents=text_chunks, metadatas=[metadata] * len(text_chunks))

def query_embeddings(query: str, filters: dict | None = None, top_k: int = 5):
    return collection.query(query_texts=[query], n_results=top_k, where=filters or {})
