from chunking.strategies.fixed_size import split_text
from chunking.schema.Chunk import Chunk
from ingestion.schema.loaded_document import LoadedDocument


def structure_aware(document: LoadedDocument, chunk_size: int = 500) -> list[Chunk]:
    texts = split_by_structure(document.raw_text, chunk_size)

    return [
        Chunk(
            text=t,
            source_file=document.source_file,
            chunk_index=i,
            strategy="structure_aware",
            section_heading=document.section_heading,
            page_number=document.page_number,
        )
        for i, t in enumerate(texts) if t.strip()
    ]


def split_by_structure(text: str, chunk_size: int) -> list[str]:
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    res = []

    for p in paragraphs:
        if len(p) <= chunk_size:
            res.append(p)
            continue

        sentences = [s for s in p.split(".") if s.strip()]
        for s in sentences:
            if len(s) <= chunk_size:
                res.append(s)
            else:
                res.extend(split_text(s, chunk_size, chunk_overlap=0))

    return res