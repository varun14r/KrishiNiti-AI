from pathlib import Path
import chromadb
from app.rag.chunker import Chunk
from app.services.ibm_services import IBMEmbeddingService

class ChromaRAGStore:
    def __init__(self, persist_dir: str, collection_name: str, embedding_service: IBMEmbeddingService):
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.embedding_service = embedding_service

    def reset(self):
        name = self.collection.name
        self.client.delete_collection(name)
        self.collection = self.client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )

    def upsert_chunks(self, chunks: list[Chunk], batch_size: int = 32):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            embeddings = self.embedding_service.embed_documents([c.text for c in batch])
            self.collection.upsert(
                ids=[f"{c.source}:{c.sequence}" for c in batch],
                documents=[c.text for c in batch],
                embeddings=embeddings,
                metadatas=[{"source": c.source, "topic": c.topic, "sequence": c.sequence} for c in batch],
            )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self.collection.count() == 0:
            return []
        embedding = self.embedding_service.embed_query(query)
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [
            {
                "text": doc,
                "document": meta.get("source", "unknown"),
                "topic": meta.get("topic", "Agriculture"),
                "score": round(max(0.0, 1.0 - float(distance)), 4),
            }
            for doc, meta, distance in zip(docs, metas, distances)
        ]
