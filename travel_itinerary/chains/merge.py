from chains.extractor import extract_from_text
from models.itinerary import Itinerary


def merge(itinerary: Itinerary, text: str) -> Itinerary:
    """Merge extracted fields with current itinerary state.

    Args:
        itinerary: Itinerary model populated with whatever fields the model can infer.
        text: Free‑form travel description.
    Returns:
        Itinerary model populated with whatever fields the model can infer.
    """

    extracted_itinerary = extract_from_text(text=text)

    if extracted_itinerary is None:
        print("Warning: No data extracted. Check your LLM API key.")
        return itinerary

    merged_itinerary = Itinerary(
        **itinerary.model_dump(),
        **extracted_itinerary.model_dump(),
    )

    return merged_itinerary
