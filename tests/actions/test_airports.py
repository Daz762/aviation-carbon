import unittest
from token import EQUAL
import os

from carbon.actions.airports import parse_airports, Airport, AirportResponse
import json


class TestAirports(unittest.TestCase):
    test_path = os.path.dirname(__file__)
    print(test_path)

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
