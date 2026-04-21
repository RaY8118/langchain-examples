from utils.data_loader import load_json_itinerary, load_directory
from chains.extractor import extract_from_text
from chains.summary import summary_from_data


# DATA_PATH = "data/sample_itineraries/itinerary_01.json"
# data = load_json_itinerary(DATA_PATH)
# print(data)

# DATA_PATH = "data/sample_itineraries"
# data = load_directory(DATA_PATH)
# print(len(data))

text = """Myself Emily.I'm planning a trip to Paris with my wife for our anniversary.
We'll be flying from New York JFK on June 5th via United Airlines flight UA123,
departing at 10am and arriving at 2pm local time.
We'll stay at the Marriott Champs-Elysees for 4 nights, checking in June 5th and checking out June 9th.
We want to visit the Louvre Museum, Eiffel Tower, and have dinner at a nice French restaurant in Montmartre."""


extracted_data = extract_from_text(text=text)
print(extracted_data)

summarized_data = summary_from_data(str(extracted_data))
print(summarized_data)
