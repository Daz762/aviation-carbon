import os
from carbon.logger.log import Logger

def action_key(carboninterface, sharpapi):
    log = Logger()

    if carboninterface is None and sharpapi is None:
        log.app_logger.error("API key is required, use -c or -s flag option to add relevant key")
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
        log.app_logger.error(f"error saving api key: {e}")

    print(f"added api key")
    return