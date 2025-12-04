from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI 
from fluency_checker.fluency_checker import FluencyChecker

# 1. Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 2. Initialize a Markdown splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

# 3. Initialize the fluency checker
checker = FluencyChecker(llm=llm, markdown_splitter=splitter)

# 4. Provide a markdown text or file
markdown_text = """
# Sample Markdown

This is a sentence that is grammatically correct.
This one maybe not be correct.

Another paragraph here.
"""

# 5. Analyze the text
segments = checker.analyze(markdown_text)

# 6. Print results
for seg in segments:
    print(f"Lines {seg.start_line}-{seg.end_line}:")
    print(f"Content: {seg.content}")
    print(f"Grammatical: {seg.grammatical}, Natural: {seg.natural}")
    if seg.suggestions:
        print(f"Suggestions: {seg.suggestions}")
    print("-" * 40)
