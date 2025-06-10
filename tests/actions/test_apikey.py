import unittest
import os

from carbon.actions.apikey import action_key

class TestApiKey(unittest.TestCase):
    test_path = os.path.dirname(__file__)
    api_key = "test-api-key"

    def test_carbonkey(self):
        os.environ["HOME"] = self.test_path
        action_key(self.api_key, None)

        f = open(f"{self.test_path}/.carbonkey")
        saved_api_key = f.read()

        self.assertEqual(self.api_key, saved_api_key, "api keys do not match")

        # clean up
        f.close()
        os.remove(os.path.join(self.test_path, ".carbonkey"))

    def test_airportkey(self):
        os.environ["HOME"] = self.test_path
        action_key(None, self.api_key)

        f = open(f"{self.test_path}/.airportkey")
        saved_api_key = f.read()

        self.assertEqual(self.api_key, saved_api_key, "api keys do not match")

        # clean up
        f.close()
        os.remove(os.path.join(self.test_path, ".airportkey"))

if __name__ == '__main__':
    unittest.main()