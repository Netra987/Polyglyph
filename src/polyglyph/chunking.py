from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    language: str
    text: str


def chunk_text(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Split text into word-based chunks of `size` words, overlapping by `overlap` words."""
    if size <= overlap:
        raise ValueError("size must be greater than overlap")
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if not piece:
            break
        chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks