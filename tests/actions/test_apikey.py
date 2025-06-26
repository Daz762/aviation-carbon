import unittest
import os

from carbon.apikeys.apikey import action_key
from carbon.apikeys.apikey import read_key

class TestApiKey(unittest.TestCase):
    test_path = os.path.dirname(__file__)
    api_key = "test-api-key"

    def test_carbonkey(self):
        os.environ["HOME"] = self.test_path
        action_key(self.api_key, None)

        f = open(f"{self.test_path}/.carboninterfacekey")
        saved_api_key = f.read()

        self.assertEqual(self.api_key, saved_api_key, "api keys do not match")

        # clean up
        f.close()
        os.remove(os.path.join(self.test_path, ".carboninterfacekey"))

    def test_airportkey(self):
        os.environ["HOME"] = self.test_path
        action_key(None, self.api_key)

        f = open(f"{self.test_path}/.sharpapikey")
        saved_api_key = f.read()

        self.assertEqual(self.api_key, saved_api_key, "api keys do not match")

        # clean up
        f.close()
        os.remove(os.path.join(self.test_path, ".sharpapikey"))

    def test_read_key(self):
        os.environ["HOME"] = self.test_path
        action_key(None, self.api_key)

        key = read_key("sharpapi")
        self.assertEqual(self.api_key, key, "api keys do not match")
        os.remove(os.path.join(self.test_path, ".sharpapikey"))

    def test_read_key_exceptions(self):
        os.environ["HOME"] = self.test_path
        with self.assertRaises(Exception) as e:
            read_key("broken")
        self.assertEqual(str(e.exception), "key retrieved must be either carbon or sharpapi")

if __name__ == '__main__':
    unittest.main()