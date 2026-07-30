import chromadb
from sentence_transformers import SentenceTransformer

from chunking.schema.chunk import Chunk
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHROMA = ROOT / "data" / "chroma"

_client = chromadb.PersistentClient(path=str(CHROMA))
_model = SentenceTransformer("all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("documents")


def store_chunks(chunks: list[Chunk], dedup_threshold: float = 0.95) -> None:
    if not chunks:
        return

    texts = [c.text for c in chunks]
    embeddings = _model.encode(texts).tolist()

    kept_chunks, kept_embeddings = [], []

    for chunk, embedding in zip(chunks, embeddings):
        if is_near_duplicate(embedding, dedup_threshold):
            print(f"Skipping near-duplicate: {chunk.source_file} chunk {chunk.chunk_index}")
            continue
        kept_chunks.append(chunk)
        kept_embeddings.append(embedding)

    if not kept_chunks:
        return

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
        embeddings=kept_embeddings,
        documents=[c.text for c in kept_chunks],
        metadatas=metadatas,
    )

def query_chunks(question: str, top_k: int = 5, strategy: str = None) -> list[dict]:
    query_embedding = _model.encode([question]).tolist()

    where = {"strategy": strategy} if strategy else None

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
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

def is_near_duplicate(embedding: list[float], threshold: float = 0.95) -> bool:
    if collection.count() == 0:
        return False

    result = collection.query(
        query_embeddings=[embedding],
        n_results=1,
    )

    if not result["distances"][0]:
        return False

    distance = result["distances"][0][0]
    similarity = 1 - distance
    return similarity > threshold

def load_all_chunks_from_chroma() -> list[Chunk]:
    all_data = collection.get(include=["documents", "metadatas"])

    chunks = []
    for text, meta in zip(all_data["documents"], all_data["metadatas"]):
        chunks.append(
            Chunk(
                text=text,
                source_file=meta["source_file"],
                chunk_index=meta["chunk_index"],
                strategy=meta["strategy"],
                section_heading=meta["section_heading"] or None,
                page_number=meta["page_number"] if meta["page_number"] != -1 else None,
            )
        )
    return chunks