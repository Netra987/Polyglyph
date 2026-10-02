import pytest

from polyglyph.chunking import chunk_text


def test_empty_text_gives_no_chunks():
    assert chunk_text("") == []


def test_short_text_gives_one_chunk():
    assert len(chunk_text("word " * 50)) == 1


def test_chunk_count_and_overlap():
    words = [f"w{i}" for i in range(500)]
    chunks = chunk_text(" ".join(words), size=200, overlap=40)
    assert len(chunks) == 3
    assert chunks[0].split()[-40:] == chunks[1].split()[:40]


def test_hindi_text_is_chunked():
    text = "भारत एक विशाल देश है " * 100
    assert len(chunk_text(text, size=50, overlap=10)) > 1


def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text("a b c", size=10, overlap=10)