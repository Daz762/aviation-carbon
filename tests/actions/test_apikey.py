import unittest
import os

from carbon.actions.apikey import action_key

class TestApiKey(unittest.TestCase):

    def test_apikey(self):
        test_path = os.path.dirname(__file__)

        api_key = "test-api-key"
        os.environ["HOME"] = test_path
        action_key(api_key)

        f = open(f"{test_path}/.carbon")
        saved_api_key = f.read()

        self.assertEqual(api_key, saved_api_key, "api keys do not match")

        # clean up
        f.close()
        os.remove(os.path.join(test_path, ".carbon"))

if __name__ == '__main__':
    unittest.main()