import requests
from dataclasses import dataclass, field
from typing import List
from carbon.actions.apikey import read_key
from columnar import columnar
from dacite import from_dict

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

def action_airport_search(api_path, city: str, country: str, name: str):
    key = read_key("sharpapi")

    if city is None and country is None and name is None:
        message = "option must be used with at least one filter (-c(ity), -co(untry) or -n(ame)"
        return message

    if country is not None and len(country) != 2:
        message = "country code must be 2 letters. E.G GB for Great Britain, US for United States etc"
        return message

    try:
        response = requests.get(
            api_path,
            params={'per_page': 100, 'city': city, 'country': country, 'name': name},
            headers={'Accept': 'application/json', 'Authorization': str(f"Bearer {key}")},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"search airports request error: {e}")

    response_data = response.json()
    if "data" not in response_data:
        message = "no data in response when searching airports"
        return message
    else:
        search_results = response_data["data"]
        if len(search_results) == 0:
            message = "no airports found, please update your search criteria"
            return message

    airport_list = []
    for airport in search_results:
        try:
            airport = from_dict(
                data_class=Airport,
                data=airport,
            )
            airport_list.append(airport)
        except Exception as e:
            print(f"error creating airport object: {e}")

    parsed_airports = parse_airports(airport_list)
    return parsed_airports


def parse_airports(airport_list: List[Airport]):
    headers = ["Name", "City", "Country", "IATA", "ID"]

    airports = []
    for airport in airport_list:
        # airports no longer in use do not have an IATA code. exclude from results
        if airport.iata == "":
            continue

        details = [airport.name, airport.city, airport.country, airport.iata, airport.id]
        airports.append(details)

    table = columnar(airports, headers, no_borders=False)
    return table
