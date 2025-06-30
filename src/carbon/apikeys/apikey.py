import os

def action_key(carboninterface, sharpapi):
    if carboninterface is None and sharpapi is None:
        message = "API key is required, use -c or -s flag option to add relevant key"
        return message

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

    message = f"added api key"
    return message

def read_key(key: str):
    if key != "carbon" and key != "sharpapi":
        raise Exception("key retrieved must be either carbon or sharpapi")
    
    if "CARBON_INTERFACE" in os.environ:
        return os.getenv["CARBON_INTERFACE"]
    
    if "SHARPAPI" in os.environ:
        return os.getenv["SHARPAPI"]

    if key == "carbon" and not os.path.exists(f"{os.environ["HOME"]}/.carboninterfacekey"):
        message = "carbon interface key does not exist. use -c or -s flag option to add relevant key"
        return message

    if key == "sharpapi" and not os.path.exists(f"{os.environ["HOME"]}/.sharpapikey"):
        message = "sharpapi key does not exist. use -c or -s flag option to add relevant key"
        return message

    if key == "carbon":
        key_path = str(f"{os.environ["HOME"]}/.carboninterfacekey")
    else:
        key_path = str(f"{os.environ["HOME"]}/.sharpapikey")

    f = open(key_path, "r")
    api_key = f.read()
    f.close()

    return api_key