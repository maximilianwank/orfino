import configparser
import logging
import logging.handlers
from typing import List, Tuple

import ccxt

import orfino.handler

logger = logging.getLogger(__file__)


def get_exchanges_and_log_handler(
    path: str,
) -> Tuple[List[ccxt.Exchange], List[logging.Handler]]:
    """
    Returns exchange instances and log handler for a given config file.
    :param path: Path to the config file.
    :return: Exchanges and log handler
    """
    # read the config file
    parser = configparser.ConfigParser()
    parser.read(filenames=path)

    # generate lists of exchanges and handlers
    exchanges = []
    handlers = []
    for section in parser.sections():
        if section in ccxt.exchanges:
            exchange_class = getattr(ccxt, section)
            exchange = exchange_class(
                config={
                    "apiKey": parser[section]["key"],
                    "secret": parser[section]["secret"],
                }
            )
            exchanges.append(exchange)
        elif section.lower() == "notifymydevice":
            handler = orfino.handler.NotifyMyDeviceHandler(
                api_key=parser[section]["key"]
            )
            handlers.append(handler)
        elif section.lower() == "timedrotatingfile":
            handler = logging.handlers.TimedRotatingFileHandler(
                filename=parser[section]["filename"],
                backupCount=parser.getint(section=section, option="count"),
                when=parser[section]["when"],
            )
            handlers.append(handler)
        else:
            logger.warning(
                f"Ignoring {section}: Is neither a valid exchange id for ccxt nor a valid log handler"
            )

    return exchanges, handlers
