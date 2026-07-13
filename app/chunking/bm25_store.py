import re
from rank_bm25 import BM25Okapi
from chunking.schema.chunk import Chunk

_bm25_index = None
_bm25_chunks = []

def build_bm25_index(chunks : list[Chunk]) -> None :
    global _bm25_index
    global _bm25_chunks

    _bm25_chunks = chunks
    tokenized_texts = [tokenize(chunk.text) for chunk in chunks]
    _bm25_index = BM25Okapi(tokenized_texts)


def query_bm25(question: str, top: int = 5) -> list[dict]:
    if _bm25_index is None:
        raise ValueError("BM25 index not built yet — call build_bm25_index first")

    tokenized_query = tokenize(question)
    scores = _bm25_index.get_scores(tokenized_query)

    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_indices = ranked_indices[:top]

    return [
        {
            "text": _bm25_chunks[i].text,
            "score": scores[i],
            "metadata": {
                "source_file": _bm25_chunks[i].source_file,
                "strategy": _bm25_chunks[i].strategy,
                "chunk_index": _bm25_chunks[i].chunk_index,
            },
        }
        for i in top_indices
    ]


def tokenize(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r'\b\w+\b', text)
