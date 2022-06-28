import logging
from unittest import TestCase
from unittest.mock import patch

import ccxt

from orfino.order_watcher import OrderWatcher


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
