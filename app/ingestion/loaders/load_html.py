from pathlib import Path
from bs4 import BeautifulSoup
from ingestion.schema.loaded_document import LoadedDocument

def load_html(path: str) -> list[LoadedDocument]:

    file_path = Path(path)
    raw_html = file_path.read_text(encoding="utf-8", errors="ignore")

    soup = BeautifulSoup(raw_html, "lxml")
    clean_text = soup.get_text(separator="\n", strip=True)

    return [
        LoadedDocument(
            source_file=str(file_path),
            file_type="html",
            raw_text=clean_text,
        )
    ]