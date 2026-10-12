import argparse
import collections
import json

import numpy as np

from polyglyph.embedding import Embedder
from polyglyph.index import DenseIndex
from polyglyph.metrics import ndcg_at_k, recall_at_k, reciprocal_rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True)
    parser.add_argument("--questions", default="eval/questions.jsonl")
    parser.add_argument("--k", type=int, default=10)
    args = parser.parse_args()

    with open(args.questions, encoding="utf-8") as f:
        questions = [json.loads(line) for line in f]

    index, model_name = DenseIndex.load(args.index)
    indexed = {c["chunk_id"] for c in index.chunks}
    usable = [q for q in questions if any(c in indexed for c in q["relevant_chunk_ids"])]
    print(f"{len(usable)} of {len(questions)} questions have their answer chunk in the index")

    embedder = Embedder(model_name)
    vectors = embedder.encode_queries([q["question"] for q in usable])
    results = index.search(vectors, k=args.k)

    rows = []
    for q, hits in zip(usable, results):
        ranked = [h["chunk_id"] for h in hits]
        rel = [c for c in q["relevant_chunk_ids"] if c in indexed]
        rows.append(
            {
                "qid": q["qid"],
                "cross": q["cross_lingual"],
                "chunk_lang": q["chunk_language"],
                "r1": recall_at_k(ranked, rel, 1),
                "r5": recall_at_k(ranked, rel, 5),
                "r10": recall_at_k(ranked, rel, 10),
                "mrr": reciprocal_rank(ranked, rel),
                "ndcg": ndcg_at_k(ranked, rel, 10),
            }
        )

    def show(label: str, subset: list[dict]) -> None:
        if not subset:
            return
        m = {key: np.mean([r[key] for r in subset]) for key in ("r1", "r5", "r10", "mrr", "ndcg")}
        print(
            f"| {label} | {len(subset)} | {m['r1']:.2f} | {m['r5']:.2f} | "
            f"{m['r10']:.2f} | {m['mrr']:.2f} | {m['ndcg']:.2f} |"
        )

    print("\n| slice | n | R@1 | R@5 | R@10 | MRR | nDCG@10 |")
    print("|---|---|---|---|---|---|---|")
    show("all", rows)
    show("same-language", [r for r in rows if not r["cross"]])
    show("cross-language", [r for r in rows if r["cross"]])
    by_lang = collections.defaultdict(list)
    for r in rows:
        by_lang[r["chunk_lang"]].append(r)
    for lang, subset in sorted(by_lang.items()):
        show(f"answer in {lang}", subset)

    misses = [r["qid"] for r in rows if r["r10"] == 0]
    print("\nnot found in top 10:", ", ".join(misses) or "none")


if __name__ == "__main__":
    main()