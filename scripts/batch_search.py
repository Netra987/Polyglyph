import argparse
import pathlib

from polyglyph.embedding import Embedder
from polyglyph.index import DenseIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="data/index_w150_balanced")
    parser.add_argument("--queries", default="eval/probe_queries.txt")
    parser.add_argument("--out", default="docs/probe_results.md")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    lines_in = pathlib.Path(args.queries).read_text(encoding="utf-8").splitlines()
    queries = [q.strip() for q in lines_in if q.strip()]

    index, model_name = DenseIndex.load(args.index)
    embedder = Embedder(model_name)
    vectors = embedder.encode_queries(queries)

    out = ["# Probe query results", "", f"Index: `{args.index}`, model: `{model_name}`", ""]
    for query, hits in zip(queries, index.search(vectors, k=args.k)):
        out += [f"## {query}", "", "| # | lang | title | score | preview |", "|---|---|---|---|---|"]
        for rank, hit in enumerate(hits, 1):
            preview = hit["text"][:80].replace("\n", " ").replace("|", " ")
            out.append(f"| {rank} | {hit['language']} | {hit['title']} | {hit['score']:.3f} | {preview} |")
        out.append("")
    pathlib.Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {len(queries)} queries to {args.out}")


if __name__ == "__main__":
    main()