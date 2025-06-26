import json
from dataclasses import dataclass
from typing import List


@dataclass
class Leg:
    departure_airport: str
    destination_airport: str


@dataclass
class Attributes:
    passengers: int
    legs: List[Leg]
    estimated_at: str
    carbon_g: float
    carbon_lb: float
    carbon_kg: float
    carbon_mt: float
    distance_unit: str
    distance_value: float


@dataclass
class EstimateData:
    id: str
    type: str
    attributes: Attributes


@dataclass
class Estimate:
    data: EstimateData
