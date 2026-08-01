import json

from ingestion.schema.loaded_document import LoadedDocument
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def load_processed(source_filename: str) -> list:
    input_path = ROOT / "data" / "processed" / f"{Path(source_filename).stem}.json"
    if not input_path.exists():
        return []
    with open(input_path) as found :
        found_as_dic = json.load(found)
        return [LoadedDocument(**doc) for doc in found_as_dic]
