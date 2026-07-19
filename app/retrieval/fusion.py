from chunking.bm25_store import query_bm25
from chunking.vector_store import query_chunks

def hybrid_query(question: str, top: int = 20) -> list[dict]:
    dense_results = query_chunks(question, top=20)
    sparse_results = query_bm25(question, top=20)

    fused = reciprocal_rank_fusion(dense_results, sparse_results)
    return fused[:top]


def reciprocal_rank_fusion(
    dense_results: list[dict],
    sparse_results: list[dict],
    k: int = 60,
    weights: tuple[float, float] = (0.5, 0.5),
) -> list[dict]:
    dense_weight, sparse_weight = weights
    scores: dict[str, float] = {}
    chunk_lookup: dict[str, dict] = {}

    for rank, result in enumerate(dense_results, start=1):
        chunk_id = get_chunk_id(result)
        scores[chunk_id] = scores.get(chunk_id, 0) + dense_weight * (1 / (k + rank))
        chunk_lookup[chunk_id] = result

    for rank, result in enumerate(sparse_results, start=1):
        chunk_id = get_chunk_id(result)
        scores[chunk_id] = scores.get(chunk_id, 0) + sparse_weight * (1 / (k + rank))
        chunk_lookup[chunk_id] = result

    ranked_ids = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)

    return [
        {**chunk_lookup[cid], "fused_score": scores[cid]}
        for cid in ranked_ids
    ]


def get_chunk_id(result: dict) -> str:
    meta = result["metadata"]
    return f"{meta['source_file']}::{meta['strategy']}::{meta['chunk_index']}"