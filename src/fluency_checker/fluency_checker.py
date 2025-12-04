from typing import List, Union
from langchain_core.language_models import BaseLanguageModel
from .splitter import MarkdownSplitter
from .prompts.fluency_prompt_pydantic import fluency_prompt
from .models import FluencySegment
import json, re

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
    
    def _sanitize_llm_json_output(self,text: str) -> str:
        # Remove ```json ... ``` fences
        fenced = re.sub(r"^```[\w]*\n", "", text.strip())
        fenced = re.sub(r"\n```$", "", fenced)
        return fenced.strip()

    def _analyze_segment(self, text: str) -> dict:
        """
        Use the LLM to evaluate fluency of a text segment.
        Returns a dict: { grammatical: bool, natural: bool, suggestions: list[str] }
        """
        prompt_str = fluency_prompt.format(text=text)
        response = self.llm.invoke(prompt_str)

        # `response` may contain:
        #   - `response.content`     (Chat model)
        #   - direct string          (Completion model)
        content = getattr(response, "content", response)
        content = self._sanitize_llm_json_output(content)
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            # If LLM returns invalid JSON, we degrade gracefully.
            parsed = {
                "grammatical": False,
                "natural": False,
                "suggestions": [content.strip()]
            }

        # Ensure required fields exist
        return {
            "grammatical": bool(parsed.get("grammatical", False)),
            "natural": bool(parsed.get("natural", False)),
            "suggestions": list(parsed.get("suggestions", [])),
        }
