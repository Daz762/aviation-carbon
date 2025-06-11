import unittest
import os
from carbon.actions.airports import action_airport_search

class TestApiKey(unittest.TestCase):
    def test_action_airport_search(self):
        action = action_airport_search(None, None, None)
