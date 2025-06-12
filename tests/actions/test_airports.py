import unittest
import requests
import os
from unittest import mock

from carbon.actions.airports import parse_airports, Airport, AirportResponse, AIRPORT_SEARCH, action_airport_search
import json

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

    if args[0] == AIRPORT_SEARCH:
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
    else:
        return MockResponse({}, 400)


class TestAirports(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_action_airport_search(self, mock_get):
        airports = action_airport_search("Lon", "GB", "Gatwick")
        self.assertIn("Test Airport", airports)
        return

    def test_parse_airports(self):
        airports = open(f"{self.test_path}/fixtures/airports.json")
        data = json.load(airports)
        airports.close()

        airport_list = []

        for airport in data["data"]:
            airport = Airport(**airport)
            airport_list.append(airport)

        assert (len(airport_list) == 3)

        parsed_airports = parse_airports(airport_list)

        self.assertRegex(parsed_airports, "Heathrow")
        self.assertRegex(parsed_airports, "Gatwick")
        self.assertNotRegex(parsed_airports, "Long Marston Airfield")
