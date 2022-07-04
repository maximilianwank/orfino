import logging.handlers
import time

from orfino.config_reader import parse_config_path, read_config
from orfino.main import main


if __name__ == "__main__":
    # read config file
    path_config = parse_config_path()
    exchanges, log_handlers = read_config(path=path_config)

    # get root logger and add handlers as specified in config
    root_logger = logging.getLogger()
    root_logger.setLevel(level=logging.DEBUG)
    for log_handler in log_handlers:
        root_logger.addHandler(log_handler)

    # log successful setup
    logging.debug(f"Sucessfully read {path_config}")

    # execute main function and log any exceptions
    try:
        main(exchanges=exchanges)
    except Exception as e:
        # something went wrong
        error_name = type(e).__name__
        logging.exception(
            msg=f"{error_name} caught in orfino main function: {e}", exc_info=True
        )
        time.sleep(60)
        exit(1)
