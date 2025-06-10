import os
from carbon.logger.log import Logger

def action_key(key):
    log = Logger()

    if key is None:
        log.app_logger.error("API key is required, use -k or --key flag option")
        return

    home = os.environ["HOME"]
    try:
        with open(os.path.join(home, ".carbon"), "w") as file:
            file.write(key)
    except Exception as e:
        log.app_logger.error(f"error saving api key: {e}")

    print(f"added api key")
    return