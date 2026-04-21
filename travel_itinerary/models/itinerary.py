from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


# --- ENUMS ---
class TravelClass(str, Enum):
    economy = "Economy"
    premium_economy = "Premium Economy"
    business = "Business"
    first = "First"


class ActivityCategory(str, Enum):
    sightseeing = "Sightseeing"
    dining = "Dining"
    transport = "Transport"
    leisure = "Leisure"
    other = "Other"


class BudgetLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# --- CORE MODELS ---
class Flight(BaseModel):
    flight_number: str
    airline: str
    departure_airport: str
    arrival_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime

    terminal: Optional[str] = None
    gate: Optional[str] = None
    seat: Optional[str] = None
    class_type: TravelClass = TravelClass.economy
    baggage_allowance: Optional[str] = None


class Accommodation(BaseModel):
    name: str
    city: str
    country: str

    check_in: date
    check_out: date

    address: Optional[str] = None
    room_type: Optional[str] = None
    confirmation_number: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    contact_phone: Optional[str] = None


class Transport(BaseModel):
    mode: str  # e.g., "Taxi", "Train", "Metro"
    pickup_location: str
    dropoff_location: str
    departure_datetime: datetime

    provider: Optional[str] = None
    arrival_datetime: Optional[datetime] = None
    booking_reference: Optional[str] = None
    cost: Optional[float] = None
    currency: str = "USD"


class Activity(BaseModel):
    name: str
    location: str
    city: str
    date: date

    category: ActivityCategory = ActivityCategory.sightseeing
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    booking_reference: Optional[str] = None
    cost: Optional[float] = None
    currency: str = "USD"
    notes: Optional[str] = None


class TravelerPreferences(BaseModel):
    budget_level: BudgetLevel = BudgetLevel.medium
    interests: List[str] = Field(default_factory=list)
    dietary_restrictions: List[str] = Field(default_factory=list)
    mobility_needs: Optional[str] = None
    preferred_language: str = "en"


class Itinerary(BaseModel):
    traveler_name: str
    trip_title: Optional[str] = None
    destination: str

    start_date: date
    end_date: date

    total_travelers: int = Field(ge=1)

    flights: List[Flight] = Field(default_factory=list)
    accommodations: List[Accommodation] = Field(default_factory=list)
    transports: List[Transport] = Field(default_factory=list)
    activities: List[Activity] = Field(default_factory=list)

    preferences: Optional[TravelerPreferences] = None
    notes: Optional[str] = None


# --- COMPLETENESS CHECK ---
from typing import Tuple, List


def get_missing_fields(itinerary: Itinerary) -> List[str]:
    """Return list of missing required fields."""
    missing = []
    if not itinerary.traveler_name:
        missing.append("traveler_name")
    if not itinerary.destination:
        missing.append("destination")
    if not itinerary.start_date:
        missing.append("start_date")
    if not itinerary.end_date:
        missing.append("end_date")
    if not itinerary.total_travelers:
        missing.append("total_travelers")
    return missing


def get_completeness(itinerary: Itinerary) -> Tuple[int, List[str]]:
    """
    Returns (completeness_score, suggestions).
    Score is 0-100 based on filled fields.
    """
    score = 0
    suggestions = []

    required_fields = [
        "traveler_name",
        "destination",
        "start_date",
        "end_date",
        "total_travelers",
    ]
    filled_required = sum(1 for f in required_fields if getattr(itinerary, f, None))
    score += int(filled_required / len(required_fields) * 60)

    optional_checks = [
        ("trip_title", "Add a trip title"),
        ("flights", "Add flight details"),
        ("accommodations", "Add accommodation"),
        ("activities", "Add some activities"),
        ("preferences", "Add traveler preferences"),
        ("notes", "Add any notes"),
    ]
    filled_optional = sum(
        1 for f, _ in optional_checks if getattr(itinerary, f, None)
    )
    score += int(filled_optional / len(optional_checks) * 40)

    for field, suggestion in optional_checks:
        if not getattr(itinerary, field, None):
            suggestions.append(suggestion)

    return score, suggestions
