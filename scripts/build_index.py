import argparse
import random

from polyglyph.embedding import DEFAULT_MODEL, Embedder
from polyglyph.index import DenseIndex, load_chunks


def sample_chunks(
    chunks: list[dict], limit: int | None, per_language: int | None
) -> list[dict]:
    rng = random.Random(42)
    if per_language:
        by_lang: dict[str, list[dict]] = {}
        for chunk in chunks:
            by_lang.setdefault(chunk["language"], []).append(chunk)
        return [
            c
            for items in by_lang.values()
            for c in rng.sample(items, min(per_language, len(items)))
        ]
    if limit and limit < len(chunks):
        return rng.sample(chunks, limit)
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=None, help="random sample of N chunks")
    parser.add_argument("--per-language", type=int, default=None, help="N chunks per language")
    parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
    parser.add_argument("--out", default="data/index")
    args = parser.parse_args()

    chunks = sample_chunks(load_chunks(args.chunks), args.limit, args.per_language)
    print(f"Embedding {len(chunks)} chunks with {args.model}")

    embedder = Embedder(args.model)
    vectors = embedder.encode_passages([c["text"] for c in chunks])
    DenseIndex.build(vectors, chunks).save(args.out, args.model)
    print("Saved index to", args.out)


if __name__ == "__main__":
    main()