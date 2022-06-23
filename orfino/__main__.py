import logging.handlers

from orfino.config_reader import read_config
from orfino.main import main


if __name__ == "__main__":
    # read config file
    exchanges, log_handlers = read_config(
        path=r"C:\Users\Max\Code\orfino\dev_config.ini"
    )

    # get root logger and add handlers as specified in config
    root_logger = logging.getLogger()
    root_logger.setLevel(level=logging.DEBUG)
    for log_handler in log_handlers:
        root_logger.addHandler(log_handler)

    # execute main function and log any exceptions
    try:
        main()
    except Exception as e:
        # something went wrong
        error_name = type(e).__name__
        logging.exception(msg=f"{error_name} in orfino main function!", exc_info=True)
        exit(1)
