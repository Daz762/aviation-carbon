from typing import Optional

import requests
from dacite import from_dict

from carbon.apikeys.apikey import read_key
from carbon.travel.data import EstimateData
from carbon.travel.parser import emissions_parser


def action_singleleg(api_path: str, apikey: str, departure: Optional[str], arrival: Optional[str], cabin: Optional[str], passengers: Optional[int], dunit: Optional[str], eunit: Optional[str]):
    # check we have departure and arrival
    if departure is None or arrival is None:
        message = "departure and arrival are required. use --help to show all available options"
        return message

    # check departure and arrival are in IATA code format
    if len(departure) != 3 or len(arrival) != 3:
        message = "3 letter IATA code must be used for departure and arrival"
        return message

    # check distance unit is valid
    if dunit.lower() != "km" and dunit.lower() != "mi":
        message = "dunit must be either 'km' or 'mi'"
        return message

    # check emissions unit is valid
    if eunit.lower() != "g" and eunit.lower() != "l" and eunit.lower() != "m" and eunit.lower() != "k":
        message = "eunit must be either 'g', 'l', 'm', or 'k'"
        return message

    if not isinstance(passengers, int):
        message = "passengers must be an number"
        return message

    # check cabin class is valid
    if cabin.lower() != "e" and cabin.lower() != "p":
        message = "cabin must be either 'e' or 'p'"
        return message

    if cabin.lower() == "e":
        cabin_class = "economy"
    else:
        cabin_class = "premium"

    try:
        response = requests.post(
            api_path,
            json={
                "type": "flight",
                "passengers": passengers,
                "legs": [
                    {"departure_airport": departure, "destination_airport": arrival, "cabin_class": cabin_class},
                ],
                "distance_unit": dunit,
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {apikey}"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"calculate carbon footprint request error: {e}")

    response_data = response.json()

    if "data" not in response_data:
        message = "no data in response when calculating carbon footprint"
        return message
    elif len(response_data["data"]) == 0:
        message = "no data in response when calculating carbon footprint"
        return message
    else:
        try:
            result = from_dict(
                data_class=EstimateData,
                data=response_data["data"],
            )
        except Exception as e:
            print(f"error creating carbon footprint object: {e}")

    message = emissions_parser(eunit, result)
    return message
