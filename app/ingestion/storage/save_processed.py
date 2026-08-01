import json
from pathlib import Path
from dataclasses import asdict

ROOT = Path(__file__).resolve().parents[3]

def save_processed(source_filename: str, documents: list) -> None:
    output_dir = ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{Path(source_filename).stem}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(doc) for doc in documents], f, indent=2)