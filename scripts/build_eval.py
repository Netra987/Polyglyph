import argparse
import collections
import json
import pathlib

from polyglyph.evalset import parse_sheet, to_eval_records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", default="eval/annotation_sheet.md")
    parser.add_argument("--out", default="eval/questions.jsonl")
    args = parser.parse_args()

    text = pathlib.Path(args.sheet).read_text(encoding="utf-8")
    records = to_eval_records(parse_sheet(text))
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    pathlib.Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_lang = collections.Counter(r["chunk_language"] for r in records)
    cross = sum(r["cross_lingual"] for r in records)
    print(f"{len(records)} questions -> {args.out}")
    print("by chunk language:", dict(by_lang), "| cross-lingual:", cross)


if __name__ == "__main__":
    main()