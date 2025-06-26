import requests

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"{self.status_code} Error")

    if args[0] == "https://airport_search/found":
        return MockResponse({
            "data": [{
                "id": "1",
                "icao": "TEST",
                "iata": "TST",
                "lid": "",
                "name": "Test Airport",
                "city": "Test City",
                "subdivision": "Test",
                "country": "GB",
                "timezone": "Europe/London",
                "elevation": 0,
                "latitude": 0,
                "longitude": 0
            }]
        }, 200)
    elif args[0] == "https://airport_search/dataempty":
        return MockResponse({"data": []}, status_code=200)
    elif args[0] == "https://airport_search/datamissing":
        return MockResponse({}, status_code=200)
    else:
        return MockResponse({}, status_code=400)