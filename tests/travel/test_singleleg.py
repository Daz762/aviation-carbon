import unittest
import os
from unittest import mock
from carbon.travel.singleleg import action_singleleg
from tests.travel.mocks import mocked_requests_post

class TestSingleLeg(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_no_departure(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key", None, "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "departure and arrival are required")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_iata(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key","LHR", "LH", "e", 1, "km", "g")
        self.assertRegex(message, "3 letter IATA code must be used for departure and arrival")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_dunit(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key","LHR", "LGW", "e", 1, "k", "g")
        self.assertRegex(message, "dunit must be either 'km' or 'mi'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_eunit(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key","LHR", "LGW", "e", 1, "km", "gr")
        self.assertRegex(message, "eunit must be either 'g', 'l', 'm', or 'k'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_cabin(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key","LHR", "LGW", "f", 1, "km", "g")
        self.assertRegex(message, "cabin must be either 'e' or 'p'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg(self, mock_get):
        message = action_singleleg("https://airport_search/found", "not_a_real_key","LGW", "LHR", "e", 1, "km", "g")
        self.assertRegex(message, "1077098")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg_data_missing(self, mock_get):
        with self.assertRaises(Exception) as context:
            action_singleleg("https://airport_search/dataempty", "not_a_real_key","LGW", "LHR", "e", 1, "km", "g")
        self.assertTrue("no data in response when calculating carbon footprint" in str(context.exception))

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_singleleg_data_empty(self, mock_get):
        with self.assertRaises(Exception) as context:
            action_singleleg("https://airport_search/datamissing", "not_a_real_key","LGW", "LHR", "e", 1, "km", "g")
        self.assertTrue("no data in response when calculating carbon footprint" in str(context.exception))
