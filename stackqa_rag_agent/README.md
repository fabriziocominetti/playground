## Stack Agent — RAG prototype with ChromaDB and local LLM

This repo is a small retrieval-augmented generation (RAG) prototype that demonstrates preparing data, creating embeddings, ingesting into a Chroma vector database, and running retrieval/LLM pipelines locally.

It is organized for experimentation — expect scripts under `src/` that handle chunking, embeddings, ingestion, and simple query tests.

## Key features

- Prepare and chunk question/answer data from CSV/parquet files
- Create embeddings and persist them to a Chroma DB
- Run basic RAG flows against a local (gguf) model
- Minimal, easy-to-read Python scripts to iterate quickly

## Repository layout

- `data/` — local datasets and Chroma DB files
  - `raw/` — source CSVs (Questions/Answers/Tags)
  - `parquet/` — intermediate parquet exports used by the pipeline
  - `chroma_db/` — Chroma database files (sqlite + segments)
  - `embeddings/` — sample embedding arrays
- `models/` — local model artifacts (example: `gemma-2b.gguf`)
- `src/` — Python scripts and modules
  - `app.py` — (optional) application entrypoint / demo server
  - `chunking.py` — logic to split long texts into chunks
  - `data_preparation.py` — prepares and normalizes raw data
  - `embeddings.py` — wrapper utilities for computing embeddings
  - `ingestion.py` — build vector DB entries from chunks + embeddings
  - `vectordb_chromadb.py` — Chroma DB utilities and helpers
  - `rag_pipeline.py` — example retrieval + generation pipeline
  - `query_test_chromadb.py` — quick script to test queries against Chroma

## Prerequisites

- macOS (this repo is OS-agnostic, but examples use zsh)
- Python 3.10+ (use a virtualenv)
- Local GPU or CPU runtime capable of running your chosen model (if using local LLM)
- `requirements.txt` in the repo root lists the Python dependencies used by the scripts

## Quick start

1. Create and activate a virtual environment

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Inspect or place model files

Place your local model file(s) in `models/` (for example `models/gemma-2b.gguf`). The scripts assume a local model path when running local LLM inference. If you plan to use an external API (OpenAI, etc.), update the code or environment accordingly.

3. Prepare data

The repo already contains sample data under `data/raw/` and parquet exports under `data/parquet/`. If you want to re-create the parquet files or change sources, run:

```zsh
python src/data_preparation.py
```

4. Chunk and embed

Create chunks from documents/questions and compute embeddings. Depending on how the scripts are organized, you can run:

```zsh
python src/chunking.py
python src/embeddings.py
```

5. Ingest into ChromaDB

This will write entries into `data/chroma_db/` (a local sqlite-backed Chroma instance in this repo):

```zsh
python src/ingestion.py
```

6. Run a quick query test

```zsh
python src/query_test_chromadb.py
# or run the pipeline
python src/rag_pipeline.py
```

7. (Optional) Launch the demo app

If `src/app.py` exposes a web/demo interface, start it like a normal Python app. For example:

```zsh
python src/app.py
```

## Utilities

- https://www.kaggle.com/datasets/stackoverflow/stacksample/data
- https://docs.bauplanlabs.com/examples/rag
- https://huggingface.co/models?library=gguf&sort=trending
