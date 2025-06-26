from typing import Optional

import requests
from dacite import from_dict

from carbon.apikeys.apikey import read_key
from carbon.travel.data import EstimateData
from carbon.travel.parser import emissions_parser


def action_multileg(api_path: str, apikey: str, legs: Optional[str], passengers: Optional[int], dunit: Optional[str],
                    eunit: Optional[str]):
    processed_legs = []
    for l in legs:
        # check format of leg input
        if len(l) != 9 or l[3] != "," or l[7] != ",":
            message = f"invalid leg input. should be DEP,ARR,CAB. got {l}. see --help for details"
            return message

        leg_details = l.split(",")
        if len(leg_details[0]) != 3:
            print(leg_details[0])
            message = f"depature not in correct format should be 3 letter IATA code, got {leg_details[0]}. see --help for more information"
            return message

        if len(leg_details[1]) != 3:
            message = f"arrival not in correct format should be 3 letter IATA code, got {leg_details[1]}. see --help for more information"
            return message

        if len(leg_details[2]) != 1 and leg_details[2].lower() != "p" and leg_details[2].lower() != "e":
            message = f"cabin class not in correct format should be 1 letter code, got {leg_details[2]}. see --help for more information"
            return message

        if leg_details[2].lower() == "e":
            cabin_class = "economy"
        else:
            cabin_class = "premium"

        processed_legs.append(
            {"departure_airport": leg_details[0], "destination_airport": leg_details[1], "cabin_class": cabin_class})

    # check distance unit is valid
    if dunit != "km" and dunit != "mi":
        message = "dunit must be either 'km' or 'mi'"
        return message

    # check emissions unit is valid
    if eunit != "g" and eunit != "l" and eunit != "m" and eunit != "k":
        message = "eunit must be either 'g', 'l', 'm', or 'k'"
        return message

    # check passengers is a number
    if not isinstance(passengers, int):
        message = "passengers must be an number"
        return message

    try:
        response = requests.post(
            api_path,
            json={
                "type": "flight",
                "passengers": passengers,
                "legs": processed_legs,
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
