import argparse
import random

from polyglyph.embedding import DEFAULT_MODEL, Embedder
from polyglyph.index import DenseIndex, load_chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=None, help="random sample of N chunks")
    parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
    parser.add_argument("--out", default="data/index")
    args = parser.parse_args()

    chunks = load_chunks(args.chunks)
    if args.limit and args.limit < len(chunks):
        chunks = random.Random(42).sample(chunks, args.limit)
    print(f"Embedding {len(chunks)} chunks with {args.model}")

    embedder = Embedder(args.model)
    vectors = embedder.encode_passages([c["text"] for c in chunks])
    DenseIndex.build(vectors, chunks).save(args.out, args.model)
    print("Saved index to", args.out)


if __name__ == "__main__":
    main()