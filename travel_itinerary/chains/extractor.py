from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from models.itinerary import Itinerary
import pandas as pd  # for CSV handling

# llm = ChatOpenRouter(model="openai/gpt-oss-120b:free")
# llm = ChatOllama(model="llama3.2:1b")
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
structured_llm = llm.with_structured_output(Itinerary)


def extract_from_text(text: str) -> Itinerary:
    """Extract itinerary details from raw text using the LLM chain.

    Args:
        text: Free‑form travel description.
    Returns:
        Itinerary model populated with whatever fields the model can infer.
    """

    # Existing implementation follows

    prompt = f"""Extract the itinerary details from this text. 
Extract only what is explicitly mentioned. Leave fields empty/None if not mentioned.

Text: {text}

Return all the details you can find."""

    result = structured_llm.invoke(prompt)
    if isinstance(result, dict):
        return Itinerary(**result)
    return result
