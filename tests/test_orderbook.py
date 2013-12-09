import unittest

from pytrade.order import BUY
from pytrade.order import Order
from pytrade.order import SELL
from pytrade.orderbook import ListOrderBook
from pytrade.orderbook import OrderBook
from pytrade.orderbook import PriorityOrderBook
from tests.factories import OrderFactory


class TestOrderBookCreation(unittest.TestCase):
    def test_bad_type(self):
        self.assertRaises(ValueError, OrderBook, 'abc')

    def test_incorrect_order_type(self):
        book = OrderBook(BUY)
        order = OrderFactory(type=SELL)
        self.assertRaises(ValueError, book.add, order)


class TestListOrderBook(unittest.TestCase):
    def _get_order_book(self, type):
        orders = [OrderFactory(type=type, value=i) for i in range(1, 11)]
        return orders, ListOrderBook(type, orders)

    def test_buy_ordering(self):
        orders, book = self._get_order_book(BUY)
        self.assertEqual(book.peek(), orders[-1])
        for order in orders[::-1]:
            self.assertEqual(order, book.pop())

    def test_sell_ordering(self):
        orders, book = self._get_order_book(SELL)
        self.assertEqual(book.peek(), orders[0])
        for order in orders:
            self.assertEqual(order, book.pop())

    def test_cancel(self):
        orders, book = self._get_order_book(SELL)
        self.assertEqual(book.peek(), orders[0])
        book.cancel(orders[0].id)
        self.assertEqual(book.peek(), orders[1])
        book.cancel(orders[2].id)
        self.assertEqual(book.pop(), orders[1])
        self.assertEqual(book.pop(), orders[3])
