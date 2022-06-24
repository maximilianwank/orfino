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
        self.mock_order_1 = {"id": "8985443494", "symbol": "BTC/USDT"}
        self.mock_order_2 = {"id": "7958465952", "symbol": "ETH/USDC"}

    @patch("ccxt.binance.fetch_open_orders")
    def test_init(self, mock_fetch_orders):
        mock_fetch_orders.return_value = self.fetch_orders_return
        order_watcher = OrderWatcher(exchange=ccxt.binance())
        self.assertEqual(len(order_watcher.open_orders), 2)

    @patch("ccxt.binance.fetch_order")
    @patch("ccxt.binance.fetch_order")
    @patch("ccxt.binance.fetch_open_orders")
    def test_log_filled_order(self, mock_fetch_orders, mock_order_1, mock_order_2):
        mock_fetch_orders.return_value = self.fetch_orders_return
        mock_order_1.return_value = self.mock_order_1
        mock_order_2.return_value = self.mock_order_2
        order_watcher = OrderWatcher(exchange=ccxt.binance())
        order_watcher.log_filled_orders()
