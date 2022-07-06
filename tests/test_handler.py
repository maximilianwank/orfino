import logging
from unittest import TestCase
from unittest.mock import patch
import urllib.error

from orfino.handler import NotifyMyDeviceHandler


class TestNotifyMyDeviceHandler(TestCase):
    def setUp(self) -> None:
        self.handler = NotifyMyDeviceHandler(api_key="foo")

    @patch("urllib.request.urlopen")
    def test_no_logging_of_url_errors(self, mock_urllib_request_urlopen):
        # let urllib raise an URLError when trying to send notify my device request
        mock_urllib_request_urlopen.side_effect = urllib.error.URLError("bar")
        # create sample log record for NotifyMyDeviceHandler.emit call
        log_record = logging.makeLogRecord(dict={"levelno": logging.ERROR})
        # check that during emit of log record no new log messages are created
        with self.assertNoLogs():
            self.handler.emit(log_record)
