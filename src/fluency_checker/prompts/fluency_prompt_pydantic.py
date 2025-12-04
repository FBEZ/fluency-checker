from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from fluency_checker.models import FluencySegmentBase

parser = PydanticOutputParser(pydantic_object=FluencySegmentBase)

fluency_prompt = PromptTemplate(
    template="""

You are a technical writer which uses a professional yet friendly tone. 
Given the following text

{text}

Reply using only the following instructions. 

{format_instructions}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

print(parser.get_format_instructions())