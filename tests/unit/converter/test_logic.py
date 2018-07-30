
import unittest

from converter.logic import (
    avrage_price_per_day,
    closing_value,
    total_trades,
    trades_per_instrument,
    trades_per_day,
)




class TestTradesLogic(unittest.TestCase):
    def setUp(self):
        self.data = [
            {
                "timestamp": "23-10-2018 6:20PM",
                "price": "200",
                "instrument": "Google-us",
                "trade_id": 1,
                "quantity": "15",
            },
            {
                "timestamp": "10-11-2018 6:20PM",
                "price": "600",
                "instrument": "Google-us",
                "trade_id": 2,
                "quantity": "2",
            },
            {
                "timestamp": "12-10-2018 6:20PM",
                "price": "200",
                "instrument": "Facebook-us",
                "trade_id": 3,
                "quantity": "5",
            },
            {
                "timestamp": "23-11-2018 6:20PM",
                "price": "200",
                "instrument": "Facebook-us",
                "trade_id": 4,
                "quantity": "20",
            },
        ]

    def test_trades_per_day(self):
        results = trades_per_day(self.data)
        expected = [
            {
                "timestamp": "23-11-2018 6:20PM",
                "price": "200",
                "instrument": "Facebook-us",
                "trade_id": 4,
                "quantity": "20",
            },
            {
                "timestamp": "23-10-2018 6:20PM",
                "price": "200",
                "instrument": "Google-us",
                "trade_id": 1,
                "quantity": "15",
            },
        ]
        self.assertItemsEqual(results[23], expected)

    def test_trades_per_instrument(self):
        results = trades_per_instrument(self.data)
        expected = [
            {
                "timestamp": "23-10-2018 6:20PM",
                "price": "200",
                "instrument": "Google-us",
                "trade_id": 1,
                "quantity": "15",
            },
            {
                "timestamp": "10-11-2018 6:20PM",
                "price": "600",
                "instrument": "Google-us",
                "trade_id": 2,
                "quantity": "2",
            },
        ]
        self.assertItemsEqual(results["Google-us"], expected)

    def test_total_trade(self):
        result = total_trades(self.data)
        self.assertEqual(result, 9200)