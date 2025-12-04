from typing import List
from pydantic import BaseModel

class FluencySegmentBase(BaseModel):
    """Base model with fluency analysis fields only."""
    grammatical: bool
    natural: bool
    suggestions: List[str]

class FluencySegment(FluencySegmentBase):
    """Full segment model including metadata like line numbers and content."""
    start_line: int
    end_line: int
    content: str
