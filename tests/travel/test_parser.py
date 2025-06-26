from carbon.travel.singleleg import emissions_parser
import json
from dacite import from_dict
from carbon.travel.data import EstimateData
import unittest
import os

class TestParser(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    def test_parse_single_leg(self):
        estimate = open(f"{self.test_path}/fixtures/estimate.json")
        data = json.load(estimate)
        estimate.close()

        estimate = from_dict(
            data_class=EstimateData,
            data=data["data"],
        )

        message = emissions_parser("g", estimate)
        self.assertEqual(message, "total emmissions for this journey: 1077098 grams")

        message = emissions_parser("l", estimate)
        self.assertRegex(message, "total emmissions for this journey: 2374 pounds")

        message = emissions_parser("k", estimate)
        self.assertRegex(message, "total emmissions for this journey: 1077 kilograms")

        message = emissions_parser("m", estimate)
        self.assertRegex(message, "total emmissions for this journey: 1 tonne(s)")