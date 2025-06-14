import os
from typing import Optional


def action_key(carboninterface: Optional[str], sharpapi: Optional[str]):
    if carboninterface is None and sharpapi is None:
        print("API key is required, use -c or -s flag option to add relevant key")
        return

    if carboninterface is not None:
        file_to_write = ".carboninterfacekey"
        key = carboninterface
    else:
        file_to_write = ".sharpapikey"
        key = sharpapi

    home = os.environ["HOME"]
    try:
        with open(os.path.join(home, file_to_write), "w") as file:
            file.write(key)
    except Exception as e:
        print(f"error saving api key: {e}")

    print(f"added api key")
    return

def read_key(key: str):
    if key != "carbon" and key != "sharpapi":
        raise Exception("key retrieved must be either carbon or sharpapi")

    if key == "carbon" and not os.path.exists(f"{os.environ["HOME"]}/.carboninterfacekey"):
        print("carbon interface key does not exist. use -c or -s flag option to add relevant key")
        return

    if key == "sharpapi" and not os.path.exists(f"{os.environ["HOME"]}/.sharpapikey"):
        print("sharpapi key does not exist. use -c or -s flag option to add relevant key")
        return

    if key == "carbon":
        key_path = str(f"{os.environ["HOME"]}/.carboninterfacekey")
    else:
        key_path = str(f"{os.environ["HOME"]}/.sharpapikey")

    f = open(key_path, "r")
    api_key = f.read()
    f.close()

    return api_key