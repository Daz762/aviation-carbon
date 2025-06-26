from dataclasses import dataclass, field
from typing import List

@dataclass
class Airport:
    id: str
    icao: str
    iata: str
    lid: str
    name: str
    city: str
    subdivision: str
    country: str
    timezone: str
    elevation: int
    latitude: float
    longitude: float

@dataclass
class AirportResponse:
    data: List[Airport] = field(default_factory=list)