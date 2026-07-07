from dataclasses import dataclass
from typing import Optional
@dataclass
class LoadedDocument:
    source_file: str
    file_type: str
    raw_text: str
    section_heading: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None