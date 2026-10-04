import re

HEADER = re.compile(r"^## (Q\d+) \| chunk: (\S+) \| chunk language: (\w+)")


def parse_sheet(text: str) -> list[dict]:
    """Parse the annotation sheet into one record per chunk block."""
    records: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        match = HEADER.match(line)
        if match:
            current = {
                "qid": match.group(1),
                "chunk_id": match.group(2),
                "chunk_language": match.group(3),
                "question": "",
                "question_language": "",
                "also_relevant": [],
            }
            records.append(current)
        elif current is not None:
            _read_field(line, current)
    return records


def _read_field(line: str, record: dict) -> None:
    if line.startswith("question:"):
        record["question"] = line.removeprefix("question:").strip()
    elif line.startswith("question_language:"):
        record["question_language"] = line.removeprefix("question_language:").strip()
    elif line.startswith("also_relevant:"):
        rest = line.removeprefix("also_relevant:")
        record["also_relevant"] = [x.strip() for x in rest.split(",") if x.strip()]


def to_eval_records(blocks: list[dict]) -> list[dict]:
    """Keep answered blocks and shape them as eval questions."""
    out = []
    for block in blocks:
        if not block["question"]:
            continue
        q_lang = block["question_language"] or block["chunk_language"]
        out.append(
            {
                "qid": block["qid"],
                "question": block["question"],
                "question_language": q_lang,
                "chunk_language": block["chunk_language"],
                "cross_lingual": q_lang != block["chunk_language"],
                "relevant_chunk_ids": [block["chunk_id"], *block["also_relevant"]],
            }
        )
    return out