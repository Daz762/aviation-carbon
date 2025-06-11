import requests
from dataclasses import dataclass, field
from typing import List
from carbon.actions.apikey import read_key
from typing import Optional

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

AIRPORT_SEARCH = "https://sharpapi.com/api/v1/airports"

def action_airport_search(city: Optional[str], country: Optional[str], name: Optional[str]):
    key = read_key("sharpapi")

    if city is None and country is None and name is None:
        print("option must be used with at least one filter (-c(ity), -co(untry) or -n(ame)")
        return

    if country is not None and len(country) != 2:
        print("country code must be 2 letters. E.G GB for Great Britain, US for United States etc")
        return

    try:
        response = requests.get(
            AIRPORT_SEARCH,
            params={'per_page': 100, 'city': city, 'country': country, 'name': name},
            headers={'Accept': 'application/json', 'Authorization': str(f"Bearer {key}")},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"search airports request error: {e}")

    response_data = response.json()
    if "data" in response_data:
        airport_list = []
        for airport in response_data["data"]:
            try:
                airport = Airport(**airport)
                airport_list.append(airport)
            except Exception as e:
                print(f"error creating airport object: {e}")
    else:
        print(f"no airport data found: {response_data}")

    print(airport_list)


def parse_airports(airport_list: List[Airport]):
    return


def action_airport_details(uuid: str):
    return
