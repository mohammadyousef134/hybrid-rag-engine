from ingestion.schema.loaded_document import LoadedDocument
from chunking.schema.Chunk import Chunk

def fixed_size(
        document : LoadedDocument,
        chunk_size : int = 500,
        chunk_overlap : int = 50,
) -> list[Chunk] :
    texts = split_text(document, chunk_size, chunk_overlap)
    return [
        Chunk(
            text=text,
            source_file=document.source_file,
            chunk_index=i,
            strategy="fixed_size",
            section_heading=document.section_heading,
            page_number=document.page_number,
        )
        for i, text in enumerate(texts) if text.strip()
    ]


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    start = 0
    end = min(chunk_size, len(text))
    res = []
    while start < len(text):
        res.append(text[start:end])
        start += chunk_size - chunk_overlap
        end = min(start + chunk_size, len(text))
    return res

