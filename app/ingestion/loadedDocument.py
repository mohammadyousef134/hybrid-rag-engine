from dataclasses import dataclass
from typing import Optional
@dataclass
class LoadedDocument:
    source_file: str
    FileType: str
    raw_text: str
    section_heading: Optional[str] = None
    page_number: Optional[int] = None