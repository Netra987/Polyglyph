import argparse

from polyglyph.embedding import Embedder
from polyglyph.index import DenseIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="data/index_w150_balanced")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    index, model_name = DenseIndex.load(args.index)
    embedder = Embedder(model_name)
    print("Type a query (Ctrl+C to quit)")
    while True:
        try:
            query = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not query:
            continue
        vec = embedder.encode_queries([query])
        for rank, hit in enumerate(index.search(vec, k=args.k)[0], 1):
            preview = hit["text"][:120].replace("\n", " ")
            print(f"{rank}. [{hit['language']}] {hit['title']} ({hit['score']:.3f}) {preview}")


if __name__ == "__main__":
    main()