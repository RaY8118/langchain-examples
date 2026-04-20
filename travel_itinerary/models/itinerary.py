from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Flight(BaseModel):
    flight_number: Optional[str] = None
    airline: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    departure_date: Optional[str] = None
    arrival_date: Optional[str] = None
    gate: Optional[str] = None
    terminal: Optional[str] = None
    seat: Optional[str] = None
    class_type: str = "Economy"
    baggage_allowance: Optional[str] = None


class Accommodation(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    room_type: Optional[str] = None
    confirmation_number: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    contact_phone: Optional[str] = None


class Transport(BaseModel):
    mode: Optional[str] = None
    provider: Optional[str] = None
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    date: Optional[str] = None
    booking_reference: Optional[str] = None
    cost: Optional[float] = None
    currency: Optional[str] = "USD"


class Activity(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    date: Optional[str] = None
    category: str = "Sightseeing"
    booking_reference: Optional[str] = None
    cost: Optional[float] = None
    currency: Optional[str] = "USD"
    notes: Optional[str] = None


class DayPlan(BaseModel):
    date: str
    activities: List[Activity] = Field(default_factory=list)
    accommodation: Optional[Accommodation] = None
    transport: Optional[Transport] = None
    flights: List[Flight] = Field(default_factory=list)


class TravelerPreferences(BaseModel):
    budget_level: str = "medium"
    interests: List[str] = Field(default_factory=list)
    dietary_restrictions: List[Optional[str]] = Field(default_factory=list)
    mobility_needs: Optional[str] = None
    preferred_language: str = "en"


class Itinerary(BaseModel):
    traveler_name: Optional[str] = None
    traveler_email: Optional[str] = None
    trip_title: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_travelers: int = 1
    flights: List[Flight] = Field(default_factory=list)
    accommodations: List[Accommodation] = Field(default_factory=list)
    transports: List[Transport] = Field(default_factory=list)
    activities: List[Activity] = Field(default_factory=list)
    preferences: Optional[TravelerPreferences] = None
    notes: Optional[str] = None
