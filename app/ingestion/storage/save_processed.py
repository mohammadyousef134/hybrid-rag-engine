import json
from pathlib import Path
from dataclasses import asdict

def save_processed(source_filename: str, documents: list) -> None:
    output_path = Path("data/processed") / f"{Path(source_filename).stem}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(doc) for doc in documents], f, indent=2)