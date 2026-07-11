from dataclasses import dataclass
from typing import Optional

@dataclass
class Chunk :
    text : str
    source_file : str
    chunk_index : int
    strategy : str
    section_heading : Optional[str] = None
    page_number : Optional[int] = None