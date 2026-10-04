import argparse
import pathlib
import random

from polyglyph.index import load_chunks

LANG_NAMES = {"hi": "Hindi", "mr": "Marathi", "en": "English"}
MIN_WORDS = 100


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", default="data/processed_w150/chunks.jsonl")
    parser.add_argument("--per-language", type=int, default=30)
    parser.add_argument("--out", default="eval/annotation_sheet.md")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    chunks = [c for c in load_chunks(args.chunks) if len(c["text"].split()) >= MIN_WORDS]
    langs = list(LANG_NAMES)

    lines = [
        "# Annotation sheet",
        "",
        "Write ONE question per chunk on the `question:` line. Leave it blank to skip.",
        "",
    ]
    number = 0
    for lang in langs:
        pool = [c for c in chunks if c["language"] == lang]
        picked = rng.sample(pool, min(args.per_language, len(pool)))
        others = [x for x in langs if x != lang]
        for i, chunk in enumerate(picked):
            number += 1
            ask = lang if i % 3 != 2 else others[(i // 3) % len(others)]
            lines += [
                f"## Q{number:03d} | chunk: {chunk['chunk_id']} | chunk language: {lang}",
                f"suggested question language: {LANG_NAMES[ask]} ({ask})",
                f"title: {chunk['title']}",
                "",
                "> " + chunk["text"].replace("\n", " "),
                "",
                "question:",
                f"question_language: {ask}",
                "also_relevant:",
                "",
            ]
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {number} chunks to {out}")


if __name__ == "__main__":
    main()