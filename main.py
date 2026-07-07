from pathlib import Path
from app.ingestion.loaders.load_txt import load_txt

loaded = load_txt("data/sample4.txt")
print(loaded)