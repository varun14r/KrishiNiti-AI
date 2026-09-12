from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.config import get_settings
from app.rag.chunker import load_knowledge_base
from app.rag.vector_store import ChromaRAGStore
from app.services.ibm_services import IBMEmbeddingService

def main():
    settings = get_settings()
    chunks = load_knowledge_base("knowledge_base", settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise SystemExit("No knowledge-base markdown files found.")
    embeddings = IBMEmbeddingService()
    store = ChromaRAGStore(settings.chroma_persist_dir, settings.chroma_collection, embeddings)
    store.upsert_chunks(chunks)
    print(f"Ingested {len(chunks)} chunks into ChromaDB collection '{settings.chroma_collection}'.")

if __name__ == "__main__":
    main()
