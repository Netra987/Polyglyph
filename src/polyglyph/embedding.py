import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "intfloat/multilingual-e5-base"


class Embedder:
    """Wraps a sentence-transformers model with e5-style prefixes."""

    def __init__(self, model_name: str = DEFAULT_MODEL, device: str | None = None):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)

    def _encode(self, texts: list[str], batch_size: int) -> np.ndarray:
        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return np.asarray(vectors, dtype="float32")

    def encode_passages(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        return self._encode([f"passage: {t}" for t in texts], batch_size)

    def encode_queries(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        return self._encode([f"query: {t}" for t in texts], batch_size)