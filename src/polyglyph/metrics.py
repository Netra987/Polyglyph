import math


def recall_at_k(ranked: list[str], relevant: list[str], k: int) -> float:
    """Share of the relevant chunks that appear in the top k."""
    if not relevant:
        return 0.0
    return len(set(ranked[:k]) & set(relevant)) / len(relevant)


def reciprocal_rank(ranked: list[str], relevant: list[str]) -> float:
    """1 / rank of the first relevant chunk, or 0 if none was retrieved."""
    rel = set(relevant)
    for position, chunk_id in enumerate(ranked, start=1):
        if chunk_id in rel:
            return 1.0 / position
    return 0.0


def ndcg_at_k(ranked: list[str], relevant: list[str], k: int) -> float:
    """Binary-relevance nDCG: rewards finding relevant chunks early."""
    rel = set(relevant)
    dcg = sum(1.0 / math.log2(i + 1) for i, c in enumerate(ranked[:k], start=1) if c in rel)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(rel), k) + 1))
    return dcg / ideal if ideal else 0.0