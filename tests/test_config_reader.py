import configparser
import os

from unittest import TestCase
from logging.handlers import TimedRotatingFileHandler

from orfino.config_reader import get_exchanges_and_log_handler
from orfino.handler import NotifyMyDeviceHandler


class TestReadConfig(TestCase):
    def setUp(self) -> None:
        self.path_config_sample = "testconfig.ini"
        self.path_log = "orfino.log"
        parser = configparser.ConfigParser()
        d = {
            "binance": {"key": "foo", "secret": "bar"},
            "notifymydevice": {"key": "baz"},
            "timedrotatingfile": {
                "filename": self.path_log,
                "count": "90",
                "when": "D",
            },
        }
        parser.read_dict(d)
        with open(self.path_config_sample, "w") as f:
            parser.write(f)

    def tearDown(self) -> None:
        try:
            os.remove(self.path_config_sample)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.path_log)
        except FileNotFoundError:
            pass

    def test_wololo(self):
        exchanges, handlers = get_exchanges_and_log_handler(self.path_config_sample)
        self.assertEqual("Binance", exchanges[0].name)
        self.assertIsInstance(handlers[0], NotifyMyDeviceHandler)
        self.assertIsInstance(handlers[1], TimedRotatingFileHandler)
