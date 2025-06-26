from typing import Optional
from carbon.travel.data import EstimateData
from carbon.apikeys.apikey import read_key
import requests

def action_multileg(api_path: str, legs: Optional[str], cabin: Optional[str], passengers: Optional[int], dunit: Optional[str], eunit: Optional[str]):
    # check legs
    print(legs)


    # ToDo - break these checks out into one block
    # check distance unit is valid
    if dunit != "km" and dunit != "mi":
        message = "dunit must be either 'km' or 'mi'"
        return message

    # check emissions unit is valid
    if eunit != "g" and eunit != "l" and eunit != "m" and eunit != "k":
        message = "eunit must be either 'g', 'l', 'm', or 'k'"
        return message

    if not isinstance(passengers, int):
        message = "passengers must be an number"
        return message

    # check cabin class is valid
    if cabin != "e" and cabin != "p":
        message = "cabin must be either 'e' or 'p'"
        return message

    if cabin == "e":
        cabin_class = "economy"
    else:
        cabin_class = "premium"

    try:
        key = read_key("carbon")
        response = requests.post(
            api_path,
            json={
                "type": "flight",
                "passengers": passengers,
                "legs": [

                ],
                "distance_unit": dunit,
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"calculate carbon footprint request error: {e}")

    return