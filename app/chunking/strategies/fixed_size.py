from ingestion.schema.loaded_document import LoadedDocument
from chunking.schema.Chunk import Chunk

def fixed_size(
        document : LoadedDocument,
        chunk_size : int = 500,
        chunk_overlap : int = 50,
) -> list[Chunk] :

    start = 0
    end = min(chunk_size, len(document.raw_text))
    idx = 0
    res = []
    while start < len(document.raw_text) :
        text = document.raw_text[start:end]
        source = document.source_file
        chunk_index = idx
        strategy = "fixed_size"
        section_heading = document.section_heading
        page_number = document.page_number
        res.append(
            Chunk(
                text = text,
                source_file = source,
                chunk_index = chunk_index,
                strategy = strategy,
                section_heading = section_heading,
                page_number = page_number,
            )
        )
        start += chunk_size - chunk_overlap
        end = min(start + chunk_size, len(document.raw_text))
        idx += 1
    return res
