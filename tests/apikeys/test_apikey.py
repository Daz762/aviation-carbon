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

    def test_read_key_env(self):
        carbon_key_reset = False
        if "CARBON_INTERFACE" in os.environ:
            carbon_key = os.environ.get("CARBON_INTERFACE")
            del os.environ["CARBON_INTERFACE"]
            carbon_key_reset = True

        sharpapi_key_reset = False
        if "SHARPAPI" in os.environ:
            sharpapi = os.environ.get("SHARPAPI")
            del os.environ["SHARPAPI"]
            sharpapi_key_reset = True

        os.environ["CARBON_INTERFACE"] = "test"
        key = read_key("carbon")
        self.assertEqual(key, "test")

        os.environ["SHARPAPI"] = "test"
        key = read_key("sharpapi")
        self.assertEqual(key, "test")

        if carbon_key_reset:
            os.environ["CARBON_INTERFACE"] = carbon_key

        if sharpapi_key_reset:
            os.environ["SHARPAPI"] = sharpapi

    def test_read_key_file(self):
        # if the user has environment variables set for these values save them so they can be wiped for testing
        carbon_key_reset = False
        if "CARBON_INTERFACE" in os.environ:
            carbon_key = os.environ.get("CARBON_INTERFACE")
            del os.environ["CARBON_INTERFACE"]
            carbon_key_reset = True

        sharpapi_key_reset = False
        if "SHARPAPI" in os.environ:
            sharpapi = os.environ.get("SHARPAPI")
            del os.environ["SHARPAPI"]
            sharpapi_key_reset = True

        os.environ["HOME"] = self.test_path
        action_key(None, self.api_key)

        key = read_key("sharpapi")
        self.assertEqual(self.api_key, key, "api keys do not match")
        os.remove(os.path.join(self.test_path, ".sharpapikey"))

        # re-apply values saved from earlier in the test back to environment variables.
        if carbon_key_reset:
            os.environ["CARBON_INTERFACE"] = carbon_key

        if sharpapi_key_reset:
            os.environ["SHARPAPI"] = sharpapi

    def test_read_key_exceptions(self):
        os.environ["HOME"] = self.test_path
        with self.assertRaises(Exception) as e:
            read_key("broken")
        self.assertEqual(str(e.exception), "key retrieved must be either carbon or sharpapi")

if __name__ == '__main__':
    unittest.main()