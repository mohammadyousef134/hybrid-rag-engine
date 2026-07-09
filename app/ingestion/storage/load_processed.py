import json

from ingestion.schema.loaded_document import LoadedDocument
from pathlib import Path

def load_processed(src : str) -> list[LoadedDocument] :
    path = Path("data/processed") / f"{Path(src).stem}.json"

    if not path.exists() :
        return []
    with open(path) as found :
        found_as_dic = json.load(found)
        return [LoadedDocument(**doc) for doc in found_as_dic]
