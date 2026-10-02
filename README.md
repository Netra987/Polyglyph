# Polyglyph

> Ask in any language. Get evidence-backed answers. Measured, not guessed.

A multilingual, multimodal retrieval-augmented generation (RAG) system for
Hindi, Marathi and English, built with evaluation at its core.

## Status
- [x] Repo, CI, chunking pipeline
- [x] Wikipedia corpus (hi / mr / en)
- [ ] Embeddings and vector index
- [ ] Hand-built eval set and metrics
- [ ] Hybrid search (BM25 + dense) and reranker
- [ ] Multimodal ingestion (PDF, scans, audio)
- [ ] Cited answers, translation, voice output
- [ ] Live demo

## Corpus
README.md: 100%|███████████████████████| 131k/131k [00:00<00:00, 16.6MB/s]
C:\Users\netra\polyglyph\.venv\Lib\site-packages\huggingface_hub\file_download.py:149: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\Users\netra\.cache\huggingface\hub\datasets--wikimedia--wikipedia. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the`HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
To support symlinks on Windows, you either need to activate Developer Modeor to run Python as an administrator. In order to activate developer mode,see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
  warnings.warn(message)
Resolving data files: 100%|████████████| 41/41 [00:00<00:00, 18617.13it/s]
{'hi': {'docs': 600, 'chunks': 7666}, 'mr': {'docs': 600, 'chunks': 3973},'en': {'docs': 600, 'chunks': 21128}}
'[WinError 10038] An operation was attempted on something that is not a socket' thrown while requesting GET https://huggingface.co/datasets/wikimedia/wikipedia/resolve/b04c8d1ceb2f5cd4588862100d08de323dccfbaa/20231101.en/train-00000-of-00041.parquet
Retrying in 1s [Retry 1/5].

## Roadmap
Retrieval first, measured with recall@k, MRR and nDCG, then multimodal input
and multi-format output.