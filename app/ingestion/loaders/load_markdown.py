from pathlib import Path
import re
from ingestion.schema.loaded_document import LoadedDocument


def load_markdown(path : str) -> list[LoadedDocument] :
    file_path = Path(path)
    raw_text = file_path.read_text(encoding="utf-8", errors= "ignore")
    sections = split_markdown(raw_text)

    return [
        LoadedDocument(
            source_file=str(file_path),
            file_type="md",
            raw_text=content.strip(),
            section_heading=heading,
        )
        for heading, content in sections
        if content.strip()
    ]

def split_markdown(text : str) -> list[tuple[str, str]] :
    pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches :
        return [None, text]

    res = []
    if matches[0].start() > 0 :
        if text[:matches[0].start()].strip() :
            res.append((None, text[:matches[0].start()]))

    for i, match in enumerate(matches):
        heading = match.group(2)
        content = text[match.end() : matches[i + 1].start() if i < len(matches) - 1 else len(text)]
        res.append((heading, content))
    return res