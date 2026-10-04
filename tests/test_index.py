import numpy as np

from polyglyph.index import DenseIndex


def test_search_returns_closest_vector_first():
    vectors = np.array([[1, 0], [0, 1], [0.7071, 0.7071]], dtype="float32")
    chunks = [{"chunk_id": "a"}, {"chunk_id": "b"}, {"chunk_id": "c"}]
    index = DenseIndex.build(vectors, chunks)
    hits = index.search(np.array([[1, 0]], dtype="float32"), k=2)[0]
    assert hits[0]["chunk_id"] == "a"
    assert hits[0]["score"] > hits[1]["score"]


def test_save_and_load_roundtrip(tmp_path):
    vectors = np.eye(3, dtype="float32")
    chunks = [{"chunk_id": str(i)} for i in range(3)]
    DenseIndex.build(vectors, chunks).save(str(tmp_path), "dummy-model")
    loaded, model_name = DenseIndex.load(str(tmp_path))
    assert model_name == "dummy-model"
    assert len(loaded.chunks) == 3