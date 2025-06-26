import requests
from carbon.travel.data import EstimateData
from dacite import from_dict

def do_request(api_path, apikey, request_data):
    try:
        response = requests.post(
            api_path,
            json=request_data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {apikey}"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"calculate carbon footprint request error: {e}")

    response_data = response.json()

    print(f"response: {response_data}")

    if "data" not in response_data:
        raise Exception("no data in response when calculating carbon footprint")
    elif len(response_data["data"]) == 0:
        raise Exception("no data in response when calculating carbon footprint")
    else:
        try:
            result = from_dict(
                data_class=EstimateData,
                data=response_data["data"],
            )
        except Exception as e:
            print(f"error creating carbon footprint object: {e}")

    return result