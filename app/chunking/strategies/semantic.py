import re
import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion.schema.loaded_document import LoadedDocument
from chunking.schema.chunk import Chunk
from chunking.schema.chunk import Chunk, next_chunk_index


_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic(document: LoadedDocument, threshold: float = 0.25) -> list[Chunk]:
    sentences = _split_into_sentences(document.raw_text)

    if len(sentences) <= 1:
        return _wrap_as_chunks([document.raw_text], document)

    boundaries = _find_boundaries(sentences, threshold)
    texts = _group_into_chunks(sentences, boundaries)

    return _wrap_as_chunks(texts, document)


def _split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _find_boundaries(sentences: list[str], threshold: float) -> list[int]:
    embeddings = _model.encode(sentences)
    boundaries = [0]
    current_chunk_embeddings = [embeddings[0]]

    for i in range(1, len(sentences)):
        chunk_avg = np.mean(current_chunk_embeddings, axis=0)
        sim = _cosine_similarity(chunk_avg, embeddings[i])

        if sim < threshold:
            boundaries.append(i)
            current_chunk_embeddings = [embeddings[i]]
        else:
            current_chunk_embeddings.append(embeddings[i])

    return boundaries


def _group_into_chunks(sentences: list[str], boundaries: list[int]) -> list[str]:
    chunks = []
    for i in range(len(boundaries)):
        start = boundaries[i]
        end = boundaries[i + 1] if i + 1 < len(boundaries) else len(sentences)
        chunks.append(" ".join(sentences[start:end]))
    return chunks


def _cosine_similarity(a, b) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def _wrap_as_chunks(texts: list[str], document: LoadedDocument) -> list[Chunk]:
    return [
        Chunk(
            text=t,
            source_file=document.source_file,
            chunk_index=next_chunk_index(document.source_file),
            strategy="semantic",
            section_heading=document.section_heading,
            page_number=document.page_number,
        )
        for i, t in enumerate(texts) if t.strip()
    ]