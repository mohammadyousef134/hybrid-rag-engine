import chromadb
from sentence_transformers import SentenceTransformer

from chunking.schema.chunk import Chunk
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHROMA = ROOT / "data" / "chroma"

_client = chromadb.PersistentClient(path=str(CHROMA))
_model = SentenceTransformer("all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("documents")


def store_chunks(chunks: list[Chunk]) -> None:
    if not chunks:
        return

    texts = [c.text for c in chunks]
    embeddings = _model.encode(texts).tolist()

    ids = [f"{c.source_file}::{c.strategy}::{c.chunk_index}" for c in chunks]

    metadatas = [
        {
            "source_file": c.source_file,
            "chunk_index": c.chunk_index,
            "strategy": c.strategy,
            "section_heading": c.section_heading or "",
            "page_number": c.page_number if c.page_number is not None else -1,
        }
        for c in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

def query_chunks(question: str, top: int = 5, strategy: str = None) -> list[dict]:
    query_embedding = _model.encode([question]).tolist()

    where = {"strategy": strategy} if strategy else None

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top,
        where=where,
    )

    return [
        {
            "text": doc,
            "metadata": meta,
            "distance": dist,
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]