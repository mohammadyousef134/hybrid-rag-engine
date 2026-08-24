# Hybrid RAG Engine

A retrieval-augmented generation pipeline that combines dense (vector) and
sparse (BM25) retrieval, fused with Reciprocal Rank Fusion and reranked with
a cross-encoder before generating a cited, verifiable answer.

## Features

- **Hybrid retrieval** — dense embedding search (Chroma) and sparse keyword
  search (BM25) combined via Reciprocal Rank Fusion, so results aren't
  limited to either approach's blind spots.
- **Cross-encoder reranking** — fused candidates are re-scored with
  `ms-marco-MiniLM-L-6-v2` before being handed to the LLM, improving
  precision over raw fusion.
- **Three pluggable chunking strategies** — `fixed_size`,
  `structure_aware`, and `semantic`, selectable per ingest run and directly
  comparable via the evaluation harness.
- **Cited, verifiable answers** — every claim in a generated answer is
  tagged with its source chunk; a separate verification pass checks each
  citation actually supports the claim it's attached to.
- **Multi-format ingestion** — `.txt`, `.md`, `.html`, and `.pdf`, with a
  parsed-document cache so re-ingesting doesn't re-parse unchanged files.
- **Evaluation harness** — a golden question set graded with LLM-as-judge
  for answer correctness, plus Precision@k / Recall@k / MRR to measure
  retrieval quality independently of generation quality.

## Pipeline

```
ingest:  document (.txt/.md/.html/.pdf) -> chunk -> embed -> store (Chroma + BM25)
ask:     question -> hybrid retrieve (dense + sparse) -> fuse -> rerank -> generate answer
```

## Setup

1. Clone the repo and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   cp .env.example .env
   ```
   Get a key at https://aistudio.google.com/apikey

## Usage

**Step 1 — Ingest your documents.** This reads every supported file in
`data/raw/`, chunks it, and stores it in the vector database. You must run
this at least once before asking questions:
```
python main.py ingest
```

Options:

| Option | Description |
|---|---|
| `--files <path> [<path> ...]` | Ingest specific files instead of everything in `data/raw/` |
| `--strategy fixed_size\|structure_aware\|semantic` | Chunking strategy (default: `fixed_size`) |
| `--clear` | Wipe the existing vector store before ingesting |

**Step 2 — Ask a question:**
```
python main.py ask "What is a hypervisor?"
```

Options:

| Option | Description |
|---|---|
| `--top-k <n>` | Number of chunks to use as context (default: 3) |
| `--verify-citations` | Run a second pass checking that each citation is actually supported |

## Evaluation

The `data/eval/golden_qa.json` file holds a set of question/expected-answer
pairs used to measure the pipeline's quality. **Run `python main.py ingest`
first** — the eval scripts read from whatever is already stored, they don't
ingest anything themselves.

```
python evaluation/run_eval.py
```

Reports answer accuracy (via LLM-as-judge grading) plus retrieval quality —
Precision@k, Recall@k, and MRR — measuring whether the right source document
was actually retrieved, independent of whether the final answer was correct.

To compare chunking strategies against each other:
```
python app/evaluation/comparison_strategies.py
```

Both scripts process the golden set in batches of 7 with a 60-second pause
between batches, to stay under the Gemini free tier's 15-requests-per-minute
limit (each question uses 2 requests: one to generate the answer, one to
grade it).

## Project structure

```
app/
  ingestion/    load documents (.txt/.md/.html/.pdf), with a JSON cache
  chunking/     fixed_size / structure_aware / semantic strategies, Chroma + BM25 storage
  retrieval/    hybrid fusion (RRF) + cross-encoder reranking
  generation/   Gemini-based answer generation with citations
  evaluation/   LLM-as-judge grading, retrieval metrics, strategy comparison
data/
  raw/          source documents
  processed/    cached parsed documents (gitignored)
  chroma/       persistent vector store (gitignored)
  eval/         golden_qa.json — the evaluation question set
main.py         CLI entrypoint (ingest / ask)
evaluation/run_eval.py   runs the full golden set through the pipeline
```
