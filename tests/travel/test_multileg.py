import os
import unittest
from unittest import mock

from carbon.travel.multileg import action_multileg
from tests.travel.mocks import mocked_requests_post


class TestSingleLeg(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_dunit(self, mock_get):
        message = action_multileg("https://airport_search/found", "not_a_real_key", ("LHR,HND,P", "HND,LAX,P"), 1, "k",
                                  "g")
        self.assertRegex(message, "dunit must be either 'km' or 'mi'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_eunit(self, mock_get):
        message = action_multileg("https://airport_search/found", "not_a_real_key", ("LHR,HND,P", "HND,LAX,P"), 1, "km",
                                  "gr")
        self.assertRegex(message, "eunit must be either 'g', 'l', 'm', or 'k'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_legs(self, mock_get):
        message = action_multileg("https://airport_search/found", "not_a_real_key", ("LHR,HND,PR", "HND,LAX,P"), 1, "km",
                                  "g")
        self.assertRegex(message, "invalid leg input. should be DEP,ARR,CAB. got LHR,HND,PR. see --help for details")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_invalid_cabin(self, mock_get):
        message = action_multileg("https://airport_search/found", "not_a_real_key", ("LHR,HND,G", "HND,LAX,P"), 1,
                                  "km",
                                  "g")
        self.assertRegex(message, "cabin must be either 'e' or 'p'")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_multileg(self, mock_get):
        message = action_multileg("https://airport_search/found", "not_a_real_key",("LHR,HND,P", "HND,LAX,P"), 1, "km", "g")
        self.assertRegex(message, "1077098")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_multileg_data_missing(self, mock_get):
        with self.assertRaises(Exception) as context:
            action_multileg("https://airport_search/dataempty", "not_a_real_key",("LHR,HND,P", "HND,LAX,P"), 1, "km", "g")
        self.assertTrue("no data in response when calculating carbon footprint" in str(context.exception))


    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_multileg_data_empty(self, mock_get):
        with self.assertRaises(Exception) as context:
            action_multileg("https://airport_search/datamissing", "not_a_real_key",("LHR,HND,P", "HND,LAX,P"), 1, "km", "g")
        self.assertTrue("no data in response when calculating carbon footprint" in str(context.exception))
