from pathlib import Path

from ingestion.schema.loaded_document import LoadedDocument

def load_txt(path: str) -> list[LoadedDocument]:
    file_path = Path(path)
    raw_text = file_path.read_text(encoding="utf-8", errors="ignore")

    return [
        LoadedDocument(
            source_file=str(file_path),
            file_type="txt",
            raw_text=raw_text,
        )
    ]