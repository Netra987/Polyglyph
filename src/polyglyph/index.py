import json
import pathlib

import faiss
import numpy as np


def load_chunks(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


class DenseIndex:
    def __init__(self, index: faiss.Index, chunks: list[dict]):
        self.index = index
        self.chunks = chunks

    @classmethod
    def build(cls, embeddings: np.ndarray, chunks: list[dict]) -> "DenseIndex":
        if len(embeddings) != len(chunks):
            raise ValueError("embeddings and chunks must have the same length")
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        return cls(index, chunks)

    def search(self, query_vectors: np.ndarray, k: int = 5) -> list[list[dict]]:
        scores, ids = self.index.search(query_vectors, k)
        results = []
        for row_scores, row_ids in zip(scores, ids):
            hits = []
            for score, i in zip(row_scores, row_ids):
                if i == -1:
                    continue
                hits.append({**self.chunks[i], "score": float(score)})
            results.append(hits)
        return results

    def save(self, directory: str, model_name: str) -> None:
        path = pathlib.Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "faiss.index"))
        with open(path / "chunks.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(chunk, ensure_ascii=False) + "\n" for chunk in self.chunks)
        with open(path / "meta.json", "w", encoding="utf-8") as f:
            json.dump({"model": model_name}, f)

    @classmethod
    def load(cls, directory: str) -> tuple["DenseIndex", str]:
        path = pathlib.Path(directory)
        index = faiss.read_index(str(path / "faiss.index"))
        chunks = load_chunks(str(path / "chunks.jsonl"))
        with open(path / "meta.json", encoding="utf-8") as f:
            model_name = json.load(f)["model"]
        return cls(index, chunks), model_name