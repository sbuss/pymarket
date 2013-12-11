import unittest

from pymarket.order import BUY
from pymarket.order import SELL
from pymarket.orderbook import ListOrderBook
from pymarket.orderbook import OrderBook
from pymarket.orderbook import PriorityOrderBook
from tests.factories import OrderFactory


class TestOrderBookCreation(unittest.TestCase):
    def test_bad_type(self):
        self.assertRaises(ValueError, OrderBook, 'abc')

    def test_incorrect_order_type(self):
        book = OrderBook(BUY)
        order = OrderFactory(type=SELL)
        self.assertRaises(ValueError, book.add, order)


class _BaseTestOrderBook(object):
    """Subclasses must define cls.ORDER_BOOK_CLASS"""
    ORDER_BOOK_CLASS = None

    def get_order_book(self, type):
        orders = [OrderFactory(type=type, value=i) for i in range(1, 11)]
        return orders, self.ORDER_BOOK_CLASS(type, orders)

    def test_buy_ordering(self):
        orders, book = self.get_order_book(BUY)
        self.assertEqual(book.peek(), orders[-1])
        for order in orders[::-1]:
            self.assertEqual(order, book.pop())

    def test_sell_ordering(self):
        orders, book = self.get_order_book(SELL)
        self.assertEqual(book.peek(), orders[0])
        for order in orders:
            self.assertEqual(order, book.pop())

    def test_cancel(self):
        orders, book = self.get_order_book(SELL)
        self.assertEqual(book.peek(), orders[0])
        book.cancel(orders[0].id)
        self.assertEqual(book.peek(), orders[1])
        book.cancel(orders[2].id)
        self.assertEqual(book.pop(), orders[1])
        self.assertEqual(book.pop(), orders[3])


class TestListOrderBook(_BaseTestOrderBook, unittest.TestCase):
    ORDER_BOOK_CLASS = ListOrderBook


class TestPriorityOrderBook(_BaseTestOrderBook, unittest.TestCase):
    ORDER_BOOK_CLASS = PriorityOrderBook
