import argparse
import json
import pathlib

from datasets import load_dataset

from polyglyph.chunking import chunk_text

SNAPSHOT = "20231101"  # check the dataset page for the current snapshot names
LANGS = {"hi": "भारत", "mr": "भारत", "en": "India"}
MIN_CHARS = 1500


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=200, help="words per chunk")
    parser.add_argument("--overlap", type=int, default=40, help="overlapping words")
    parser.add_argument("--max-docs", type=int, default=600, help="articles per language")
    parser.add_argument("--out-dir", default="data/processed")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stats = {}
    with open(out_dir / "chunks.jsonl", "w", encoding="utf-8") as f:
        for lang, keyword in LANGS.items():
            ds = load_dataset(
                "wikimedia/wikipedia", f"{SNAPSHOT}.{lang}", split="train", streaming=True
            )
            docs = chunks = 0
            for row in ds:
                text = row["text"]
                if len(text) < MIN_CHARS or keyword not in text:
                    continue
                for i, piece in enumerate(chunk_text(text, args.size, args.overlap)):
                    record = {
                        "chunk_id": f"{lang}-{row['id']}-{i}",
                        "doc_id": f"{lang}-{row['id']}",
                        "title": row["title"],
                        "language": lang,
                        "text": piece,
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    chunks += 1
                docs += 1
                if docs >= args.max_docs:
                    break
            stats[lang] = {"docs": docs, "chunks": chunks}
    print(stats)


if __name__ == "__main__":
    main()