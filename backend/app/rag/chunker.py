from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class Chunk:
    text: str
    source: str
    topic: str
    sequence: int

def chunk_text(text: str, source: str, topic: str, size: int = 1200, overlap: int = 180) -> list[Chunk]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    start = 0
    seq = 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            boundary = text.rfind(". ", start, end)
            if boundary > start + size // 2:
                end = boundary + 1
        part = text[start:end].strip()
        if part:
            chunks.append(Chunk(part, source, topic, seq))
            seq += 1
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

def load_knowledge_base(base_dir: str, size: int = 1200, overlap: int = 180) -> list[Chunk]:
    chunks = []
    for path in sorted(Path(base_dir).glob("*.md")):
        topic = path.stem.replace("_", " ").title()
        chunks.extend(chunk_text(path.read_text(encoding="utf-8"), path.name, topic, size, overlap))
    return chunks
