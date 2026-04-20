import json
import random
from datetime import datetime, timedelta
from pathlib import Path

AIRLINES = ["United Airlines", "Delta", "American Airlines", "British Airways", "Emirates", "Lufthansa", "Air France", "Qatar Airways", "Singapore Airlines", "Cathay Pacific"]
AIRPORTS = {
    "JFK": "New York", "LAX": "Los Angeles", "ORD": "Chicago", "SFO": "San Francisco", "MIA": "Miami",
    "LHR": "London", "CDG": "Paris", "FRA": "Frankfurt", "AMS": "Amsterdam", "MAD": "Madrid",
    "NRT": "Tokyo", "SIN": "Singapore", "HKG": "Hong Kong", "DXB": "Dubai", "BKK": "Bangkok",
    "SYD": "Sydney", "MEL": "Melbourne", "ROM": "Rome", "BCN": "Barcelona", "IST": "Istanbul"
}
CITIES = ["New York", "Los Angeles", "London", "Paris", "Tokyo", "Singapore", "Dubai", "Sydney", "Rome", "Barcelona", "Amsterdam", "Bangkok", "Hong Kong", "Istanbul", "Madrid", "Berlin", "Milan", "Vienna", "Lisbon", "Prague"]
HOTELS = ["Marriott", "Hilton", "Hyatt", "InterContinental", "Four Seasons", "Ritz-Carlton", "Sheraton", "Westin", "Novotel", "Ibis", "Radisson", "Crowne Plaza", "W Hotels", "St. Regis", "Mandarin Oriental"]
ACTIVITIES_BY_CITY = {
    "New York": [("Statue of Liberty", "Landmark", "Manhattan"), ("Central Park", "Park", "Manhattan"), ("Times Square", "Attraction", "Midtown"), ("Brooklyn Bridge", "Landmark", "Brooklyn"), ("Museum of Modern Art", "Museum", "Manhattan")],
    "London": [("British Museum", "Museum", "Bloomsbury"), ("Tower of London", "Landmark", "Tower Hill"), ("Buckingham Palace", "Landmark", "Westminster"), ("Big Ben", "Landmark", "Westminster"), ("London Eye", "Attraction", "Southbank")],
    "Paris": [("Eiffel Tower", "Landmark", "Champ de Mars"), ("Louvre Museum", "Museum", "1st arrondissement"), ("Notre-Dame", "Landmark", "Île de la Cité"), ("Champs-Élysées", "Shopping", "8th arrondissement"), ("Montmartre", "Neighborhood", "18th arrondissement")],
    "Tokyo": [("Senso-ji Temple", "Temple", "Asakusa"), ("Shibuya Crossing", "Attraction", "Shibuya"), ("Tokyo Tower", "Landmark", "Minato"), ("Meiji Shrine", "Temple", "Shibuya"), ("Tsukiji Market", "Food", "Tsukiji")],
    "Rome": [("Colosseum", "Landmark", "Centro Storico"), ("Vatican Museums", "Museum", "Vatican City"), ("Trevi Fountain", "Landmark", "Centro Storico"), ("Pantheon", "Landmark", "Centro Storico"), ("Roman Forum", "Archaeological", "Centro Storico")],
    "Barcelona": [("Sagrada Familia", "Landmark", "Eixample"), ("Park Güell", "Park", "Gràcia"), ("La Rambla", "Shopping", "Ciutat Vella"), ("Gothic Quarter", "Neighborhood", "Ciutat Vella"), ("Camp Nou", "Sports", "Les Corts")],
    "Sydney": [("Sydney Opera House", "Landmark", "Circular Quay"), ("Harbour Bridge", "Landmark", "Sydney Harbour"), ("Bondi Beach", "Beach", "Bondi"), ("Taronga Zoo", "Attraction", "Mosman"), ("Blue Mountains", "Nature", "Blue Mountains")],
    "Dubai": [("Burj Khalifa", "Landmark", "Downtown"), ("Dubai Mall", "Shopping", "Downtown"), ("Palm Jumeirah", "Landmark", "Palm Jumeirah"), ("Dubai Marina", "Neighborhood", "Marina"), ("Desert Safari", "Adventure", "Desert")],
    "Amsterdam": [("Rijksmuseum", "Museum", "Museumplein"), ("Anne Frank House", "Museum", "Centrum"), ("Van Gogh Museum", "Museum", "Museumplein"), ("Vondelpark", "Park", "Oud-West"), ("Anne Frank House", "Historical", "Centrum")],
    "Singapore": [("Marina Bay Sands", "Landmark", "Marina Bay"), ("Gardens by the Bay", "Park", "Marina Bay"), ("Sentosa Island", "Beach", "Sentosa"), ("Chinatown", "Neighborhood", "Chinatown"), ("Universal Studios", "Theme Park", "Sentosa")]
}
TRANSPORT_MODES = ["Taxi", "Uber", "Metro", "Bus", "Train", "Rental Car", "Shuttle", "Ferry"]
ACTIVITY_CATEGORIES = ["Sightseeing", "Museum", "Food & Dining", "Shopping", "Adventure", "Nature", "Sports", "Cultural", "Relaxation", "Nightlife"]


def random_date(start_date, days_range):
    return start_date + timedelta(days=random.randint(0, days_range))


def random_time():
    return f"{random.randint(0, 23):02d}:{random.choice([0, 15, 30, 45]):02d}"


def generate_flight(origin, dest, date, flight_num):
    dep_time = f"{random.randint(6, 20):02d}:{random.choice([0, 15, 30, 45]):02d}"
    duration = random.randint(2, 14)
    arr_hour = (int(dep_time[:2]) + duration) % 24
    arr_time = f"{arr_hour:02d}:{dep_time[3:]}"
    arr_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1 if arr_hour < int(dep_time[:2]) else 0)).strftime("%Y-%m-%d")
    return {
        "flight_number": f"{random.choice(['UA', 'DL', 'AA', 'BA', 'EK', 'LH'])}{flight_num:04d}",
        "airline": random.choice(AIRLINES),
        "departure_airport": origin,
        "arrival_airport": dest,
        "departure_time": dep_time,
        "arrival_time": arr_time,
        "departure_date": date,
        "arrival_date": arr_date,
        "gate": f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 50)}",
        "terminal": str(random.randint(1, 8)),
        "seat": f"{random.randint(1, 35)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}",
        "class_type": random.choice(["Economy", "Premium Economy", "Business", "First"]),
        "baggage_allowance": random.choice(["1 checked bag", "2 checked bags", "Carry-on only"])
    }


def generate_hotel(city, check_in, check_out):
    return {
        "name": f"{random.choice(HOTELS)} {city}",
        "address": f"{random.randint(1, 999)} {random.choice(['Main', 'Park', 'Ocean', 'Grand', 'Central'])} Street",
        "city": city,
        "country": city if city in ["New York", "Los Angeles", "Miami", "San Francisco"] else "USA" if city in ["Chicago", "Boston", "Seattle"] else "UK" if city == "London" else "France" if city == "Paris" else "Japan" if city == "Tokyo" else "Australia" if city == "Sydney" else "UAE" if city == "Dubai" else "Netherlands" if city == "Amsterdam" else "Singapore",
        "check_in": check_in,
        "check_out": check_out,
        "room_type": random.choice(["Standard Room", "Deluxe Room", "Suite", "Executive Suite", "Presidential Suite"]),
        "confirmation_number": f"CONF{random.randint(100000, 999999)}",
        "amenities": random.sample(["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar", "Room Service", "Parking", "Airport Shuttle", "Business Center"], k=random.randint(3, 6)),
        "contact_phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    }


def generate_transport(mode, pickup, dropoff, date):
    if mode in ["Taxi", "Uber", "Shuttle"]:
        return {
            "mode": mode,
            "provider": mode if mode != "Uber" else "Uber",
            "pickup_location": pickup,
            "dropoff_location": dropoff,
            "departure_time": random_time(),
            "arrival_time": random_time(),
            "date": date,
            "booking_reference": f"TR{random.randint(10000, 99999)}",
            "cost": round(random.uniform(15, 150), 2),
            "currency": "USD"
        }
    elif mode in ["Metro", "Bus"]:
        return {
            "mode": mode,
            "provider": "Public Transport",
            "pickup_location": pickup,
            "dropoff_location": dropoff,
            "departure_time": random_time(),
            "arrival_time": random_time(),
            "date": date,
            "booking_reference": None,
            "cost": round(random.uniform(2, 10), 2),
            "currency": "USD"
        }
    else:
        return {
            "mode": mode,
            "provider": random.choice(["Hertz", "Enterprise", "Avis", "Budget"]),
            "pickup_location": pickup,
            "dropoff_location": dropoff,
            "departure_time": random_time(),
            "arrival_time": random_time(),
            "date": date,
            "booking_reference": f"CAR{random.randint(100000, 999999)}",
            "cost": round(random.uniform(50, 200), 2),
            "currency": "USD"
        }


def generate_activity(city, date, day_num):
    city_activities = ACTIVITIES_BY_CITY.get(city, [("City Tour", "Sightseeing", "City Center")])
    activity = random.choice(city_activities)
    start_hour = random.randint(9, 16)
    end_hour = start_hour + random.randint(1, 4)
    return {
        "name": activity[0],
        "description": f"Visit and enjoy {activity[0]} in {city}",
        "location": f"{activity[2]}, {city}",
        "city": city,
        "start_time": f"{start_hour:02d}:{random.choice([0, 30]):02d}",
        "end_time": f"{end_hour:02d}:{random.choice([0, 30]):02d}",
        "date": date,
        "category": activity[1],
        "booking_reference": f"ACT{random.randint(10000, 99999)}",
        "cost": round(random.uniform(0, 150), 2),
        "currency": "USD",
        "notes": random.choice([None, "Wear comfortable shoes", "Bring camera", "Advance booking recommended", "Free cancellation"])
    }


def generate_itinerary(itinerary_num, dest_city, duration, trip_type):
    start_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
    end_date = start_date + timedelta(days=duration)
    cities = [dest_city] + random.sample([c for c in CITIES if c != dest_city], k=min(2, duration // 4))
    origin = random.choice(list(AIRPORTS.keys()))
    dest_airport = random.choice([k for k, v in AIRPORTS.items() if v == dest_city] or list(AIRPORTS.keys())[:5])

    flights = []
    if trip_type in ["multi-city", "round-trip"]:
        flights.append(generate_flight(origin, dest_airport, start_date.strftime("%Y-%m-%d"), itinerary_num * 2))
        if trip_type == "round-trip":
            flights.append(generate_flight(dest_airport, origin, end_date.strftime("%Y-%m-%d"), itinerary_num * 2 + 1))

    accommodations = []
    check_in = start_date.strftime("%Y-%m-%d")
    check_out = end_date.strftime("%Y-%m-%d")
    accommodations.append(generate_hotel(dest_city, check_in, check_out))

    activities = []
    for day in range(duration):
        current_date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
        city = cities[min(day // (duration // len(cities) + 1), len(cities) - 1)]
        num_activities = random.randint(1, 3)
        for _ in range(num_activities):
            activities.append(generate_activity(city, current_date, day))

    transports = []
    for _ in range(min(duration, 3)):
        trans_date = (start_date + timedelta(days=random.randint(0, duration - 1))).strftime("%Y-%m-%d")
        transports.append(generate_transport(random.choice(TRANSPORT_MODES), "Hotel", "Activity Venue", trans_date))

    return {
        "traveler_name": f"Traveler {itinerary_num}",
        "traveler_email": f"traveler{itinerary_num}@example.com",
        "trip_title": f"{trip_type.title()} Trip to {dest_city}",
        "destination": dest_city,
        "start_date": check_in,
        "end_date": check_out,
        "total_travelers": random.randint(1, 4),
        "flights": flights,
        "accommodations": accommodations,
        "transports": transports,
        "activities": activities,
        "preferences": {
            "budget_level": random.choice(["low", "medium", "high"]),
            "interests": random.sample(ACTIVITY_CATEGORIES, k=random.randint(2, 4)),
            "dietary_restrictions": random.sample([None, "Vegetarian", "Vegan", "Gluten-free", "Nut allergy"], k=random.randint(0, 2)),
            "mobility_needs": None,
            "preferred_language": "en"
        },
        "notes": f"Excited to explore {dest_city}!"
    }


TRIP_TYPES = ["round-trip", "one-way", "multi-city"]
ITINERARIES = []

itinerary_specs = [
    (CITIES[0], 5, "round-trip"), (CITIES[1], 7, "round-trip"), (CITIES[2], 4, "one-way"), (CITIES[3], 6, "multi-city"),
    (CITIES[4], 8, "round-trip"), (CITIES[5], 3, "one-way"), (CITIES[6], 5, "round-trip"), (CITIES[7], 10, "multi-city"),
    (CITIES[8], 4, "round-trip"), (CITIES[9], 6, "one-way"), (CITIES[10], 7, "round-trip"), (CITIES[11], 5, "multi-city"),
    (CITIES[12], 4, "round-trip"), (CITIES[13], 6, "one-way"), (CITIES[14], 8, "round-trip"), (CITIES[15], 3, "one-way"),
    (CITIES[16], 5, "round-trip"), (CITIES[17], 7, "multi-city"), (CITIES[18], 4, "round-trip"), (CITIES[19], 6, "one-way"),
    (CITIES[0], 14, "multi-city"), (CITIES[2], 10, "round-trip"), (CITIES[4], 12, "round-trip")
]

for i, (city, duration, trip_type) in enumerate(itinerary_specs, 1):
    ITINERARIES.append(generate_itinerary(i, city, duration, trip_type))

output_dir = Path(__file__).parent / "sample_itineraries"
output_dir.mkdir(exist_ok=True)

for i, itinerary in enumerate(ITINERARIES, 1):
    filename = output_dir / f"itinerary_{i:02d}.json"
    with open(filename, "w") as f:
        json.dump(itinerary, f, indent=2)

print(f"Generated {len(ITINERARIES)} itineraries in {output_dir}")
