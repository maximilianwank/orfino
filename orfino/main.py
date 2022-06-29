import time
from typing import List

import ccxt

from orfino.order_watcher import OrderWatcher


def main(exchanges: List[ccxt.Exchange]):
    order_watchers = [OrderWatcher(exchange=exchange) for exchange in exchanges]
    while True:
        for ow in order_watchers:
            ow.check_and_notify()
        time.sleep(60)
