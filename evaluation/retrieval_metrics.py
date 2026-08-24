def precision_at_k(retrieved_chunks: list[dict], expected_source_file: str) -> float:
    if not retrieved_chunks:
        return 0.0

    relevant = sum(
        1 for chunk in retrieved_chunks
        if chunk["metadata"]["source_file"] == expected_source_file
    )
    return relevant / len(retrieved_chunks)


def recall_at_k(retrieved_chunks: list[dict], expected_source_file: str) -> float:

    found = any(
        chunk["metadata"]["source_file"] == expected_source_file
        for chunk in retrieved_chunks
    )
    return 1.0 if found else 0.0


def reciprocal_rank(retrieved_chunks: list[dict], expected_source_file: str) -> float:
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        if chunk["metadata"]["source_file"] == expected_source_file:
            return 1.0 / rank
    return 0.0


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0