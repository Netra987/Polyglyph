import argparse
import random

import numpy as np
from transformers import AutoTokenizer

from polyglyph.index import load_chunks

parser = argparse.ArgumentParser()
parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
parser.add_argument("--model", default="intfloat/multilingual-e5-base")
parser.add_argument("--n", type=int, default=3000)
args = parser.parse_args()

tok = AutoTokenizer.from_pretrained(args.model)
chunks = load_chunks(args.chunks)
chunks = random.Random(0).sample(chunks, min(args.n, len(chunks)))
for lang in ["hi", "mr", "en"]:
    lens = np.array(
        [len(tok(c["text"], truncation=False)["input_ids"]) for c in chunks if c["language"] == lang]
    )
    if len(lens):
        print(
            f"{lang}: n={len(lens)} median={int(np.median(lens))} "
            f"max={lens.max()} over512={int((lens > 512).sum())} ({np.mean(lens > 512):.1%})"
        )