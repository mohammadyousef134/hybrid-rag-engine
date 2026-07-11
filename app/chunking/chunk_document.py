from ingestion.schema.loaded_document import LoadedDocument
from chunking.schema.chunk import Chunk
from chunking.strategies.fixed_size import fixed_size
from chunking.strategies.structure_aware import structure_aware
from chunking.strategies.semantic import semantic


def chunk_document(document: LoadedDocument, strategy: str = "fixed_size", **kwargs) -> list[Chunk]:
    strategies = {
        "fixed_size": fixed_size,
        "structure_aware": structure_aware,
        "semantic": semantic,
    }

    if strategy not in strategies:
        raise ValueError(f"Unknown strategy: {strategy}")

    return strategies[strategy](document, **kwargs)