from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from models.itinerary import Itinerary
from llm.get_llm import local_llm as llm

structured_llm = llm.with_structured_output(Itinerary)


def extract_from_text(text: str) -> Itinerary:
    """Extract itinerary details from raw text using the LLM chain.

    Args:
        text: Free‑form travel description.
    Returns:
        Itinerary model populated with whatever fields the model can infer.
    """

    parser = PydanticOutputParser(pydantic_object=Itinerary)
    prompt = PromptTemplate(
        template="""
    You are an information extraction system.

    Extract structured travel data from the text.

    {format_instructions}

    Text:
    {text}
    """,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    formatted_prompt = prompt.format(text=text)
    result = structured_llm.invoke(formatted_prompt)
    if isinstance(result, dict):
        return Itinerary(**result)
    return result  # type: ignore
