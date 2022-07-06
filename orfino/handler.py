import http.client
import json
import logging.handlers
import typing
import urllib.request
import urllib.error


logger = logging.getLogger(__name__)


def send_notify_my_device_message(
    api_key: str, title: str, body: str, log_url_errors: bool
) -> typing.Optional[http.client.HTTPResponse]:
    """
    Send a message through the Notify My Device service to your smartphone
    :param api_key: API key generated on notifymydevice.com/myapplications
    :param title: Title of the message (encoding utf-8)
    :param body: Body of the message (encoding utf-8)
    :param log_url_errors: Decide whether to log URLErrors or not. Must be set to
    false if used in emit method of some log handler to avoid RecursionError
    :return: Response of
    """
    data = json.dumps({"ApiKey": api_key, "PushTitle": title, "PushText": body})
    req = urllib.request.Request(
        url="https://www.notifymydevice.com/push",
        data=data.encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if log_url_errors:
            logger.warning(f"Unable to send notification via Notify My Device: {e}")
        response = None
    return response


class NotifyMyDeviceHandler(logging.Handler):
    def __init__(
        self, api_key: str, level: typing.Union[int, str] = logging.NOTSET
    ) -> None:
        """
        Create log handler forwarding log records to the Notify My Device API
        You need an account on notifymydevice.com and create an application there
        :param api_key: API key generated on notifymydevice.com/myapplications
        :param level: Logging level
        """
        self.api_key = api_key
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno < 30:
            symbol = "ℹ️"
        elif record.levelno < 40:
            symbol = "⚠️"
        else:
            symbol = "🆘"
        send_notify_my_device_message(
            api_key=self.api_key,
            title=f"{symbol} {record.filename}",
            body=self.format(record=record),
            log_url_errors=False,
        )
