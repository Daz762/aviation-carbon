import requests
from typing import List
from carbon.airports.data import Airport
from columnar import columnar
from dacite import from_dict


def action_airport_search(api_path, apikey, city, country, name):
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
            headers={'Accept': 'application/json', 'Authorization': str(f"Bearer {apikey}")},
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
