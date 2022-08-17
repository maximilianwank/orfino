import logging
from unittest import TestCase
from unittest.mock import patch

import ccxt

from orfino.order_watcher import ccxt_order_to_text
from orfino.order_watcher import OrderWatcher


class TestCcxtOrderToText(TestCase):
    def setUp(self) -> None:
        # sample order from https://docs.ccxt.com/en/latest/manual.html#order-structure
        self.sample_order_structure = {
            "id": "12345-67890:09876/54321",  # string
            "clientOrderId": "abcdef-ghijklmnop-qrstuvwxyz",  # a user-defined clientOrderId, if any
            "datetime": "2017-08-17 12:42:48.000",  # ISO8601 datetime of 'timestamp' with milliseconds
            "timestamp": 1502962946216,  # order placing/opening Unix timestamp in milliseconds
            "lastTradeTimestamp": 1502962956216,  # Unix timestamp of the most recent trade on this order
            "status": "closed",  # 'open', 'closed', 'canceled', 'expired', 'rejected'
            "symbol": "ETH/BTC",  # symbol
            "type": "limit",  # 'market', 'limit'
            "timeInForce": "GTC",  # 'GTC', 'IOC', 'FOK', 'PO'
            "side": "buy",  # 'buy', 'sell'
            "price": 0.06917684,  # float price in quote currency (may be empty for market orders)
            "average": 0.06917684,  # float average filling price
            "amount": 1.5,  # ordered amount of base currency
            "filled": 1.1,  # filled amount of base currency
            "remaining": 0.4,  # remaining amount to fill
            "cost": 0.076094524,  # 'filled' * 'price' (filling price used where available)
            "trades": [...],  # a list of order trades/executions
            "fee": {  # fee info, if available
                "currency": "BTC",  # which currency the fee is (usually quote)
                "cost": 0.0009,  # the fee amount in that currency
                "rate": 0.002,  # the fee rate (if available)
            },
            "info": {...},  # the original unparsed order structure as is
        }

    def test_with_cost(self):
        r = ccxt_order_to_text(self.sample_order_structure)
        self.assertEqual(r, "Closed: Buying 1.5 ETH for 0.076094524 BTC")

    def test_without_cost(self):
        # see what happens without cost
        del self.sample_order_structure["cost"]
        r = ccxt_order_to_text(self.sample_order_structure)
        self.assertEqual(r, "Closed: Buying 1.5 ETH for BTC")


class TestOrderWatcher(TestCase):
    def setUp(self) -> None:
        self.fetch_orders_return = [
            {"id": "8985443494", "symbol": "BTC/USDT"},
            {"id": "7958465952", "symbol": "ETH/USDC"},
        ]
        self.mock_order_1 = {
            "id": "8985443494",
            "symbol": "BTC/USDT",
            "status": "filled",
            "side": "buy",
            "amount": 0.125,
        }
        self.mock_order_2 = {"id": "7958465952", "symbol": "ETH/USDC", "status": "open"}

    @patch("ccxt.binance.fetch_open_orders")
    def test_init(self, mock_fetch_orders):
        mock_fetch_orders.return_value = self.fetch_orders_return
        order_watcher = OrderWatcher(exchange=ccxt.binance())
        self.assertEqual(len(order_watcher.open_orders), 2)

    @patch("ccxt.binance.fetch_order")
    @patch("ccxt.binance.fetch_open_orders")
    def test_get_new_and_log_filled_orders(self, mock_fetch_orders, mock_order):
        mock_fetch_orders.return_value = self.fetch_orders_return
        mock_order.side_effect = [self.mock_order_1, self.mock_order_2]
        order_watcher = OrderWatcher(exchange=ccxt.binance())
        with self.assertLogs("orfino.order_watcher") as ow_logs:
            order_watcher._notify_filled_orders_and_remove_from_local_list()
        self.assertEqual(len(order_watcher.open_orders), 1)
        self.assertEqual(len(ow_logs.output), 1)
