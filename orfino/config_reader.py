import argparse
import configparser
import logging
import logging.handlers
from typing import List, Tuple

import ccxt

import orfino.handler

logger = logging.getLogger(__file__)


def parse_config_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("path_config", type=str)
    x = parser.parse_args()
    return x.path_config


def read_config(
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
            config = {
                "apiKey": parser[section]["key"],
                "secret": parser[section]["secret"],
            }
            if "password" in parser[section]:
                config["password"] = parser[section]["password"]
            exchange = exchange_class(config=config)
            exchange.logger.setLevel(logging.INFO)
            exchanges.append(exchange)
        elif section.lower() == "notifymydevice":
            handler = orfino.handler.NotifyMyDeviceHandler(
                api_key=parser[section]["key"]
            )
            handler.setLevel(level=logging.INFO)
            handlers.append(handler)
        elif section.lower() == "timedrotatingfile":
            handler = logging.handlers.TimedRotatingFileHandler(
                filename=parser[section]["filename"],
                backupCount=parser.getint(section=section, option="count"),
                when=parser[section]["when"],
            )
            handler.setLevel(level=logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s [pid %(process)d] %(levelname)-8s %(module)s.%(funcName)s():%(lineno)d %(message)s"
            )
            handler.setFormatter(formatter)
            handlers.append(handler)
        else:
            logger.warning(
                f"Ignoring {section}: It's neither a valid exchange id for ccxt nor a valid log handler"
            )

    return exchanges, handlers
