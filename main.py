from pathlib import Path
from app.ingestion.loaders.load_txt import load_txt
from app.ingestion.loaders.load_markdown import load_markdown

# loaded = load_txt("data/sample4.txt")
# print(loaded)

loaded = load_markdown("data/sample.md")
print(loaded)