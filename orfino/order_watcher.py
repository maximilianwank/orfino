from datetime import datetime, timedelta

from orfino.data_model import Order

import ccxt


class OrderWatcher:
    def __init__(self, exchange: ccxt.Exchange):
        self.exchange = exchange
        # pretend that last call for all trades was an hour ago
        self._update_orders_last_call = datetime.now() - timedelta(hours=1)
        self._update_open_orders()

    def _update_open_orders(self):
        # first of all ensure that there is no ip ban
        if self._update_orders_last_call + timedelta(minutes=20) < datetime.now():
            self._update_orders_last_call = datetime.now()
            # we took care of respective limits
            self.exchange.options["warnOnFetchOpenOrdersWithoutSymbol"] = False
            open_orders_raw = self.exchange.fetch_open_orders()
            self.exchange.options["warnOnFetchOpenOrdersWithoutSymbol"] = True
            # save new open orders
            self.open_orders = [
                Order(id=oo["info"]["orderId"], symbol=oo["info"]["symbol"])
                for oo in open_orders_raw
            ]

    def log_filled_orders(self):
        pass
