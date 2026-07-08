from ingestion.schema.loaded_document import LoadedDocument
from pathlib import Path
import pdfplumber

def load_pdf(path : str) -> list[LoadedDocument] :
    file_path = Path(path)

    documents = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start = 1) :
            text = page.extract_text()
            if not text.strip() :
                continue

            documents.append(
                LoadedDocument(
                    source_file = str(file_path),
                    file_type = "pdf",
                    raw_text = text.strip(),
                    page_number = page_number,
                )
            )
    return documents

