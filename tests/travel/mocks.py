import requests

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"{self.status_code} Error")

    if args[0] == "https://airport_search/found":
        return MockResponse({
            "data": {
                "id": "d60edacc-cf6c-4da7-b5de-c538de4ce5ee",
                "type": "estimate",
                "attributes": {
                    "passengers": 2,
                    "legs": [
                        {
                            "departure_airport": "SFO",
                            "destination_airport": "YYZ"
                        },
                        {
                            "departure_airport": "YYZ",
                            "destination_airport": "SFO"
                        }
                    ],
                    "estimated_at": "2020-07-24T02:25:50.837Z",
                    "carbon_g": 1077098,
                    "carbon_lb": 2374,
                    "carbon_kg": 1077,
                    "carbon_mt": 1,
                    "distance_unit": "km",
                    "distance_value": 7454.15
                }
            },
        }, status_code=200)
    elif args[0] == "https://airport_search/dataempty":
        return MockResponse({"data":{}}, status_code=400)
    elif args[0] == "https://airport_search/datamissing":
        return MockResponse({}, status_code=400)