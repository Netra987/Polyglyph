import pytest

from polyglyph.metrics import ndcg_at_k, recall_at_k, reciprocal_rank


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], ["b"], 1) == 0.0
    assert recall_at_k(["a", "b", "c"], ["b"], 2) == 1.0
    assert recall_at_k(["a", "b"], ["a", "z"], 2) == 0.5


def test_reciprocal_rank():
    assert reciprocal_rank(["a", "b", "c"], ["b"]) == 0.5
    assert reciprocal_rank(["a", "b"], ["z"]) == 0.0


def test_ndcg_rewards_early_hits():
    early = ndcg_at_k(["b", "x", "y"], ["b"], 3)
    late = ndcg_at_k(["x", "y", "b"], ["b"], 3)
    assert early == pytest.approx(1.0)
    assert late == pytest.approx(0.5)


def test_ndcg_with_no_hit_is_zero():
    assert ndcg_at_k(["x", "y"], ["b"], 5) == 0.0