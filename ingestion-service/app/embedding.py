import chromadb
  from chromadb.config import Settings as ChromaSettings
  from .config import settings

  chroma_client = chromadb.Client(
      ChromaSettings(
          chroma_api_impl="rest",
          chroma_server_host="api.trychroma.com",
          chroma_server_http_port="443",
          chroma_server_ssl_enabled=True,
          anonymized_telemetry=False,
      )
  )

  chroma_client.set_settings({
      "chroma_api_key": settings.CHROMA_API_KEY,
      "tenant": settings.CHROMA_TENANT,
      "database": settings.CHROMA_DATABASE,
  })

  collection = chroma_client.get_or_create_collection("documents")

  def upsert_embedding(doc_id: str, text_chunks: list[str], metadata: dict):
      if not text_chunks:
          return
      ids = [f"{doc_id}_{i}" for i in range(len(text_chunks))]
      collection.upsert(ids=ids, documents=text_chunks, metadatas=[metadata]*len(text_chunks))

  def query_embeddings(query: str, filters: dict | None = None, top_k: int = 5):
      return collection.query(query_texts=[query], n_results=top_k, where=filters or {})

