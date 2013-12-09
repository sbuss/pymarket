import unittest

from pytrade.order import BUY, SELL, Order
from tests.factories import OrderFactory


class TestOrderCreation(unittest.TestCase):
    def test_bad_type(self):
        attrs = OrderFactory.attributes()
        attrs['type'] = 'abc'
        self.assertRaises(ValueError, Order, **attrs)

    def test_negative_amount(self):
        attrs = OrderFactory.attributes()
        attrs['amount'] = -100
        self.assertRaises(ValueError, Order, **attrs)

    def test_negative_value(self):
        attrs = OrderFactory.attributes()
        attrs['value'] = -100
        self.assertRaises(ValueError, Order, **attrs)

    def test_float_amount(self):
        attrs = OrderFactory.attributes()
        attrs['amount'] = 100.
        self.assertRaises(ValueError, Order, **attrs)

    def test_float_value(self):
        attrs = OrderFactory.attributes()
        attrs['value'] = 100.
        self.assertRaises(ValueError, Order, **attrs)

    def test_bad_user(self):
        attrs = OrderFactory.attributes()
        attrs['user'] = 'abc'
        self.assertRaises(ValueError, Order, **attrs)

    def test_good_buy(self):
        attrs = OrderFactory.attributes()
        order = Order(**attrs)
        self.assertTrue(order)
        self.assertEqual(order.type, BUY)

    def test_good_sell(self):
        attrs = OrderFactory.attributes()
        attrs['type'] = SELL
        order = Order(**attrs)
        self.assertTrue(order)
        self.assertEqual(order.type, SELL)
