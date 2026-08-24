import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "app"))

from ingestion.load_document import load_document
from chunking.chunk_document import chunk_document
from chunking.schema.chunk import reset_chunk_counter
from chunking.vector_store import store_chunks, load_all_chunks_from_chroma, clear_collection
from chunking.bm25_store import build_bm25_index
from retrieval.fusion import hybrid_query
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer, verify_citations

RAW_DIR = ROOT / "data" / "raw"
SUPPORTED_EXTENSIONS = {".txt", ".md", ".html", ".pdf"}


def discover_files() -> list[str]:
    return sorted(
        p.relative_to(ROOT).as_posix()
        for p in RAW_DIR.iterdir()
        if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def cmd_ingest(args: argparse.Namespace) -> None:
    files = args.files if args.files else discover_files()
    if not files:
        print(f"No documents found in {RAW_DIR}")
        return

    if args.clear:
        print("Clearing existing vector store...")
        clear_collection()

    total_chunks = 0
    for file_path in files:
        reset_chunk_counter(file_path)
        docs = load_document(file_path)
        for doc in docs:
            chunks = chunk_document(doc, strategy=args.strategy)
            store_chunks(chunks)
            total_chunks += len(chunks)
        print(f"Ingested {file_path} ({len(docs)} sections)")

    print(f"\nDone. {total_chunks} chunks stored using '{args.strategy}' strategy.")


def cmd_ask(args: argparse.Namespace) -> None:
    chunks = load_all_chunks_from_chroma()
    if not chunks:
        print("Vector store is empty. Run 'python main.py ingest' first.")
        return

    build_bm25_index(chunks)

    fused = hybrid_query(args.question, top_k=10)
    top_chunks = rerank(args.question, fused, top_k=args.top_k)

    answer = generate_answer(args.question, top_chunks)

    print(f"\nQuestion: {args.question}\n")
    print(f"Answer:\n{answer}\n")

    print("Sources:")
    for i, chunk in enumerate(top_chunks, start=1):
        meta = chunk["metadata"]
        print(f"  [{i}] {meta['source_file']} (chunk {meta['chunk_index']})")

    if args.verify_citations:
        print("\nCitation check:")
        print(verify_citations(answer, top_chunks))


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid RAG engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Load and index documents from data/raw/")
    ingest_parser.add_argument(
        "--files", nargs="+", default=None,
        help="Specific files to ingest (default: all supported files in data/raw/)",
    )
    ingest_parser.add_argument(
        "--strategy", choices=["fixed_size", "structure_aware", "semantic"],
        default="fixed_size", help="Chunking strategy to use (default: fixed_size)",
    )
    ingest_parser.add_argument(
        "--clear", action="store_true",
        help="Clear the existing vector store before ingesting",
    )
    ingest_parser.set_defaults(func=cmd_ingest)

    ask_parser = subparsers.add_parser("ask", help="Ask a question against the indexed documents")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to use as context (default: 3)")
    ask_parser.add_argument("--verify-citations", action="store_true", help="Run citation verification on the answer")
    ask_parser.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()