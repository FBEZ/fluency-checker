from typing import List
from langchain_core.prompts import PromptTemplate  

fluency_prompt_template = """
You are an expert English editor.

Analyze the following markdown text:

{text}

Provide a JSON object with:
- grammatical: boolean
- natural: boolean
- suggestions: list of alternative phrasings (may be empty)

Return ONLY valid JSON.
"""

fluency_prompt = PromptTemplate(
    input_variables=["text"],  # ✅ Fixed {{text}} -> {text}
    template=fluency_prompt_template
)
