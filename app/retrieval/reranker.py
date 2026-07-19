from sentence_transformers import CrossEncoder
from retrieval.fusion import hybrid_query

_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(question : str, candidates : list[dict], top : int = 5) -> list[dict] :
    if not candidates :
        return []

    pairs = [(question, candidate['text']) for candidate in candidates]
    scores = _reranker.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate['rerank_score'] = float(score)

    reranked = sorted(candidates, key = lambda x : x["rerank_score"], reverse = True)
    return reranked[:top]

def hybrid_query_reranked(question: str, top: int = 5) -> list[dict]:
    fused = hybrid_query(question, top = 20)
    return rerank(question, fused)