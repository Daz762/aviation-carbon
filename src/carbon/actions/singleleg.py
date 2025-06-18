from typing import Optional
from dataclasses import dataclass
from typing import List
from datetime import datetime

CARBON_URL = "https://www.carboninterface.com/api/v1/estimates"

@dataclass
class Leg:
    departure_airport: str
    destination_airport: str

@dataclass
class EstimateAttributes:
    passengers: int
    legs: List[Leg]
    estimated_at: datetime
    carbon_g: int
    carbon_lb: int
    carbon_kg: int
    carbon_mt: int
    distance_unit: str
    distance_value: float

@dataclass
class EstimateData:
    id: str
    type: str
    attributes: EstimateAttributes

@dataclass
class Estimate:
    data: EstimateData


def action_singleleg(departure: str, arrival: str, cabin: Optional[str], passengers: int):
    return
