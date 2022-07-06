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
        mock_urllib_request_urlopen.side_effect = urllib.error.URLError("bar")
        log_record = logging.makeLogRecord(dict={"levelno": logging.ERROR})
        with self.assertNoLogs():
            self.handler.emit(log_record)
