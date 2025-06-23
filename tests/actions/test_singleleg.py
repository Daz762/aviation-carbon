import unittest
import requests
import os
from unittest import mock
from carbon.actions.singleleg import action_singleleg


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
        return MockResponse({}, status_code=200)
    elif args[0] == "https://airport_search/dataempty":
        return MockResponse({}, status_code=400)
    elif args[0] == "https://airport_search/datamissing":
        return MockResponse({}, status_code=400)

class TestSingleLeg(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg(self, mock_get):
        emissions = action_singleleg("https://airport_search/found", "LGW", "LHR", "e", 1, "km", "g")
        print(emissions)