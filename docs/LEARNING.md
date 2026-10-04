# Learning Log

## Day 1-2: Repo, chunking, corpus

**Why do we overlap chunks, and what's the tradeoff of a bigger overlap?**
(Hint: a fact can sit on a chunk boundary and get cut in half. Overlap keeps
context on both sides. The cost is more chunks, more storage and more
duplicate results.)

**Why filter the corpus by topic instead of taking random articles?**
(Hint: I need to write test questions with known answers. A focused corpus
makes that possible and makes evaluation meaningful.)

**What does `pip install -e .` do?**
(Hint: it installs my project in "editable" mode, so Python can import
`polyglyph` from anywhere and code edits apply immediately.)

**What does CI do?**
(Hint: on every push, GitHub runs my linter and tests on a clean machine,
so a broken commit is caught early.)

## What went wrong and how I fixed it
- Push rejected: token lacked `workflow` scope. Fixed by ...

## Open questions
-