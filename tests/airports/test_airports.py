import unittest
import os
from unittest import mock
from carbon.airports.airports import parse_airports, action_airport_search
from carbon.airports.data import Airport
from tests.airports.mocks import mocked_requests_get
import json


class TestAirports(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_action_airport_search(self, mock_get):
        airports = action_airport_search("https://airport_search/found", "not_a_real_key", "Lon", "GB", "Gatwick")
        self.assertIn("Test Airport", airports)
        return

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_action_airport_search_none(self, mock_get):
        airports = action_airport_search("https://airport_search/dataempty", "not_a_real_key", "Auk", "NZ", "")
        self.assertIn("no airports found", airports)
        return

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_action_airport_search_missing(self, mock_get):
        airports = action_airport_search("https://airport_search/datamissing", "not_a_real_key", "Auk", "NZ", "")
        self.assertIn("no data in response when searching airports", airports)
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
