import os
from carbon.logger.log import Logger

def action_key(carbon, airport):
    log = Logger()

    if carbon is None and airport is None:
        log.app_logger.error("API key is required, use -c or -a flag option to add relevant key")
        return

    if carbon is not None:
        file_to_write = ".carbonkey"
        key = carbon
    else:
        file_to_write = ".airportkey"
        key = airport

    home = os.environ["HOME"]
    try:
        with open(os.path.join(home, file_to_write), "w") as file:
            file.write(key)
    except Exception as e:
        log.app_logger.error(f"error saving api key: {e}")

    print(f"added api key")
    return