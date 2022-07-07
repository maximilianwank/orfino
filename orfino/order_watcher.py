import logging
from datetime import datetime, timedelta

from orfino.data_model import Order

import ccxt


logger = logging.getLogger(__name__)


class OrderWatcher:
    def __init__(self, exchange: ccxt.Exchange):
        # keep the exchange as attribute
        self.exchange = exchange
        # pretend that last call for all trades was an hour ago
        self._update_orders_last_call = datetime.now() - timedelta(hours=1)
        self._update_open_orders_rate_limited()
        logger.info(
            f"Found {len(self.open_orders)} open orders on {exchange.name} to monitor"
        )
        for oo in self.open_orders:
            logger.debug(f" - {str(oo)}")

    def _update_open_orders_rate_limited(self) -> None:
        """
        Updating the list of open orders from the CEX. Attention: This potentially removes items from self.open_orders!
        Hence, this method is only to be called directly after handling orders that where in self.open_orders and might
        be not open anymore.
        """
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
                Order(id=oo["id"], symbol=oo["symbol"]) for oo in open_orders_raw
            ]
            logger.debug(
                f"Updated all open orders on {self.exchange.name} at {self._update_orders_last_call}"
            )

    def _notify_filled_orders_and_remove_from_local_list(self) -> None:
        """
        Log and therefore notify orders that have been filled. Filled orders are removed from self.open_orders.
        """
        # ToDo: This method does not distinguish between various not open states (closed / canceled / filled) etc.
        # see https://docs.ccxt.com/en/latest/manual.html#order-structure
        try:
            not_open_raw = [
                od
                for o in self.open_orders
                if (od := self.exchange.fetch_order(id=o.id, symbol=o.symbol))["status"]
                != "open"
            ]
        except ccxt.NetworkError as e:
            logger.warning(f"Unable to fetch open orders: {e}")
            not_open_raw = []
        # log and notify filled orders
        for fo in not_open_raw:
            coin_traded, coin_base = fo["symbol"].split("/")
            logger.info(f'{fo["side"]} {fo["amount"]} {coin_traded} for {coin_base}')
        # remove filled from list - this happens only sometimes when calling self._update_open_orders_rate_limited to
        # rate limits
        filled = [Order(id=x["id"], symbol=x["symbol"]) for x in not_open_raw]
        for fo in filled:
            self.open_orders.remove(fo)

    def check_and_notify(self):
        """
        Check for new unfilled orders (whilst respecting rate limits in this method) and notify (log) orders that have
        been filled.
        """
        self._notify_filled_orders_and_remove_from_local_list()
        self._update_open_orders_rate_limited()
