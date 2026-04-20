from models.itinerary import Itinerary
import os
import json
from typing import List
from pydantic import ValidationError


def load_json_itinerary(filepath: str) -> Itinerary:
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileExistsError:
        print("File not found")

    return Itinerary(**data)


def load_directory(directory_path: str) -> List[Itinerary]:
    itineraries = []

    for file in os.listdir(directory_path):
        if not file.endswith(".json"):
            continue
        file_path = os.path.join(directory_path, file)
        try:
            itinerary = load_json_itinerary(filepath=file_path)
            itineraries.append(itinerary)
        except ValidationError as e:
            print(f"Skipping {file} : {e}")

    return itineraries
