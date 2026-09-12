from app.rag.chunker import chunk_text

def test_chunk_text_creates_chunks():
    chunks = chunk_text("A. " * 100, "demo.md", "Demo", size=100, overlap=20)
    assert chunks
    assert all(c.source == "demo.md" for c in chunks)
