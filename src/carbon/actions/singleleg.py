from dataclasses import dataclass
from typing import List

import requests

from carbon.actions.apikey import read_key
from datetime import datetime

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


def action_singleleg(api_path: str, departure: str, arrival: str, cabin: str, passengers: int, tunit: str, runit: str):
    key = read_key("carbon")

    # check we have departure and arrival
    if departure is None and arrival is None:
        message = "departure and arrival are required. us --help to show all available options"
        return message

    # check departure and arrival are in IATA code format
    if len(departure) != 3 or len(arrival) != 3:
        message = "3 letter IATA code must be used for departure and arrival"
        return message

    # check travel unit is valid
    if tunit != "k" or tunit != "m":
        message = "tunit must be either 'k' or 'm'"
        return message

    # check result unit is valid
    if runit != "g" or runit != "l" or runit != "m" or runit != "k":
        message = "runit must be either 'g', 'l', 'm', or 'k'"
        return message

    # check cabin class is valid
    if cabin != "e" or cabin != "p":
        message = "cabin must be either 'e' or 'p'"
        return message

    try:
        response = requests.post(
            api_path,
            params={
                "type": "flight",
                "passengers": passengers,
                "distance_unit": tunit,
                "legs": [
                    {"departure": departure, "arrival": arrival, "cabin_class": cabin},
                ]
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"calculate carbon footprint request error: {e}")

    response_data = response.json()
    print(response_data)
