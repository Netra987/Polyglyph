from polyglyph.evalset import parse_sheet, to_eval_records

SHEET = """# Annotation sheet

## Q001 | chunk: hi-1-0 | chunk language: hi
suggested question language: Hindi (hi)

> पुणे महाराष्ट्र का एक शहर है।

question: पुणे किस राज्य में है?
question_language: hi
also_relevant: hi-1-1, hi-1-2

## Q002 | chunk: en-9-4 | chunk language: en

> Some English text.

question:
question_language: mr
also_relevant:
"""


def test_parse_sheet_reads_all_blocks():
    blocks = parse_sheet(SHEET)
    assert [b["qid"] for b in blocks] == ["Q001", "Q002"]
    assert blocks[0]["also_relevant"] == ["hi-1-1", "hi-1-2"]


def test_blank_questions_are_skipped():
    records = to_eval_records(parse_sheet(SHEET))
    assert len(records) == 1
    assert records[0]["relevant_chunk_ids"] == ["hi-1-0", "hi-1-1", "hi-1-2"]
    assert records[0]["cross_lingual"] is False


def test_cross_lingual_flag():
    block = {
        "qid": "Q1",
        "chunk_id": "mr-1-0",
        "chunk_language": "mr",
        "question": "Who?",
        "question_language": "en",
        "also_relevant": [],
    }
    assert to_eval_records([block])[0]["cross_lingual"] is True