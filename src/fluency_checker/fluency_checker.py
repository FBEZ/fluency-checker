from typing import List, Union
from langchain_core.language_models import BaseLanguageModel
from .splitter import MarkdownSplitter
from .models import FluencySegment

class FluencyChecker:
    """Checks fluency of markdown text using an LLM."""

    def __init__(self, llm: BaseLanguageModel, markdown_splitter: MarkdownSplitter):
        self.llm = llm
        self.splitter = markdown_splitter

    def analyze(self, input_data: Union[str, "Path"]) -> List[FluencySegment]:
        """
        Analyze either a filename or raw text.
        
        Args:
            input_data (str | Path): Markdown file path or text content.

        Returns:
            List[FluencySegment]: List of analyzed text segments.
        """
        if isinstance(input_data, str) and "\n" in input_data:
            text = input_data
        else:
            # Treat as filename
            with open(input_data, "r", encoding="utf-8") as f:
                text = f.read()

        segments = self.splitter.split_text(text)
        analyzed_segments: List[FluencySegment] = []

        current_line = 1
        for segment in segments:
            num_lines = segment.count("\n") + 1
            # Placeholder for LLM logic
            result = self._analyze_segment(segment)
            analyzed_segments.append(
                FluencySegment(
                    start_line=current_line,
                    end_line=current_line + num_lines - 1,
                    content=segment,
                    grammatical=result["grammatical"],
                    natural=result["natural"],
                    suggestions=result["suggestions"]
                )
            )
            current_line += num_lines

        return analyzed_segments

    def _analyze_segment(self, text: str) -> dict:
        """
        Placeholder method to call LLM for fluency analysis.
        Returns a dict with keys: grammatical, natural, suggestions.
        """
        # TODO: implement actual LLM logic
        return {
            "grammatical": True,
            "natural": True,
            "suggestions": [text, "this is just a test"]
        }
