from langchain_core.prompts import PromptTemplate
from llm.get_llm import local_llm as llm


def summary_from_data(itinerary_json: str) -> str:
    prompt = PromptTemplate(
        template="""
You are an expert travel assistant.

Convert the following structured itinerary data into a clear, natural, human-readable summary.

Keep it concise but informative.

Itinerary Data:
{data}
""",
        input_variables=["data"],
    )

    chain = prompt | llm
    result = chain.invoke({"data": itinerary_json})

    return str(result.content)
