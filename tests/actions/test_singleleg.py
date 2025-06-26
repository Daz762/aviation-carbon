import unittest
import requests
import os
from unittest import mock
from carbon.travel.singleleg import action_singleleg, parse_single_leg, EstimateData
import json
from dacite import from_dict


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        test_path = os.path.dirname(__file__)

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

class TestSingleLeg(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_no_departure(self, mock_get):
        message = action_singleleg("https://airport_search/found", None, "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "departure and arrival are required")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_iata(self, mock_get):
        message = action_singleleg("https://airport_search/found", "LHR", "LH", "e", 1, "km", "g")
        self.assertRegex(message, "3 letter IATA code must be used for departure and arrival")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_dunit(self, mock_get):
        message = action_singleleg("https://airport_search/found", "LHR", "LGW", "e", 1, "k", "g")
        self.assertRegex(message, "dunit must be either 'km' or 'mi'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_eunit(self, mock_get):
        message = action_singleleg("https://airport_search/found", "LHR", "LGW", "e", 1, "km", "gr")
        self.assertRegex(message, "eunit must be either 'g', 'l', 'm', or 'k'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_cabin(self, mock_get):
        message = action_singleleg("https://airport_search/found", "LHR", "LGW", "f", 1, "km", "g")
        self.assertRegex(message, "cabin must be either 'e' or 'p'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg(self, mock_get):
        message = action_singleleg("https://airport_search/found", "LGW", "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "1077098")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg_data_missing(self, mock_get):
        message = action_singleleg("https://airport_search/dataempty", "LGW", "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "no data in response when calculating carbon footprint")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg_data_empty(self, mock_get):
        message = action_singleleg("https://airport_search/datamissing", "LGW", "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "no data in response when calculating carbon footprint")

    def test_parese_single_leg(self):
        estimate = open(f"{self.test_path}/fixtures/estimate.json")
        data = json.load(estimate)
        estimate.close()

        estimate = from_dict(
            data_class=EstimateData,
            data=data["data"],
        )

        # parse grams
        message = parse_single_leg("LGW", "LHR", "g", estimate)
        self.assertRegex(message, "1077098")

        # parse lb
        message = parse_single_leg("LGW", "LHR", "l", estimate)
        self.assertRegex(message, "2374")

        # parse kg
        message = parse_single_leg("LGW", "LHR", "k", estimate)
        self.assertRegex(message, "1077")

        # parse mt
        message = parse_single_leg("LGW", "LHR", "m", estimate)
        self.assertRegex(message, "1")
