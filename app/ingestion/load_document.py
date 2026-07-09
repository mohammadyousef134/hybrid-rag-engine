from pathlib import Path

from ingestion.storage import load_processed
from ingestion.storage.save_processed import save_processed
from ingestion.loaders.load_pdf import load_pdf
from ingestion.loaders.load_txt import load_txt
from ingestion.loaders.load_html import load_html
from ingestion.loaders.load_markdown import load_markdown
from ingestion.storage.load_processed import load_processed

def load_document(path: str) -> list:
    ext = Path(path).suffix.lower().lstrip(".")

    cached = load_processed(path)
    if cached :
        return cached

    if ext == "txt":
        res = load_txt(path)
        save_processed(path, res)
        return res
    elif ext == "md":
        res = load_markdown(path)
        save_processed(path, res)
        return res
    elif ext == "html":
        res = load_html(path)
        save_processed(path, res)
        return res
    elif ext == "pdf":
        res = load_pdf(path)
        save_processed(path, res)
        return res
    else:
        raise ValueError(f"Unsupported file type: {ext}")