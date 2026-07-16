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

_counters: dict[str, int] = {}

def next_chunk_index(source_file: str) -> int:
    current = _counters.get(source_file, 0)
    _counters[source_file] = current + 1
    return current

def reset_chunk_counter(source_file: str) -> None:
    _counters[source_file] = 0