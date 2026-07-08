from pathlib import Path

from bs4 import BeautifulSoup
from pathlib import Path

from app.ingestion.loaders.load_txt import load_txt
from app.ingestion.loaders.load_markdown import load_markdown
from ingestion.loaders.load_html import load_html

# loaded = load_txt("data/sample4.txt")
# print(loaded)

# loaded = load_markdown("data/sample.md")
# print(loaded)

loaded = load_html("data/sample3.html")
print(loaded)