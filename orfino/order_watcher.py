from datetime import datetime, timedelta

from orfino.data_model import Order

import ccxt


class OrderWatcher:
    def __init__(self, exchange: ccxt.Exchange):
        # keep the exchange as attribute
        self.exchange = exchange
        # pretend that last call for all trades was an hour ago
        self._update_orders_last_call = datetime.now() - timedelta(hours=1)
        self._update_open_orders()

    def _update_open_orders(self):
        # first ensure that there is no ip ban
        if self._update_orders_last_call + timedelta(minutes=20) < datetime.now():
            self._update_orders_last_call = datetime.now()
            # we took care of respective limits - so set the option as we need it
            self.exchange.options["warnOnFetchOpenOrdersWithoutSymbol"] = False
            # get orders as loaded json
            open_orders_raw = self.exchange.fetch_open_orders()
            # set limit warning back to default value
            self.exchange.options["warnOnFetchOpenOrdersWithoutSymbol"] = True
            # save new open orders
            self.open_orders = [
                Order(id=oo['id'], symbol=oo['symbol'])
                for oo in open_orders_raw
            ]

    def log_filled_orders(self):
        print(1 + 1)
