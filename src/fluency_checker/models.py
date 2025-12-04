from typing import List
from pydantic import BaseModel

class FluencySegment(BaseModel):
    """Represents a segment of text with fluency and grammar analysis."""
    start_line: int
    end_line: int
    content: str
    grammatical: bool
    natural: bool
    suggestions: List[str]
