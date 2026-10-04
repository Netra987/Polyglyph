import argparse
import collections

from polyglyph.index import load_chunks

parser = argparse.ArgumentParser()
parser.add_argument("term")
parser.add_argument("--corpus", default="data/processed_w150/chunks.jsonl")
parser.add_argument("--index", default="data/index_w150_balanced/chunks.jsonl")
args = parser.parse_args()

for label, path in [("corpus", args.corpus), ("index ", args.index)]:
    counts = collections.Counter(c["language"] for c in load_chunks(path) if args.term in c["text"])
    print(label, dict(counts))