from typing import Protocol, List

class MarkdownSplitter(Protocol):
    """Protocol for splitting markdown text into segments."""
    
    def split_text(self, text: str) -> List[str]:
        ...
