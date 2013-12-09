import unittest

from pytrade import order
from tests.factories import OrderFactory


class TestOrderCreation(unittest.TestCase):
    def test_bad_type(self):
        attrs = OrderFactory.attributes()
        attrs['type'] = 'abc'
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_negative_amount(self):
        attrs = OrderFactory.attributes()
        attrs['amount'] = -100
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_negative_value(self):
        attrs = OrderFactory.attributes()
        attrs['value'] = -100
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_float_amount(self):
        attrs = OrderFactory.attributes()
        attrs['amount'] = 100.
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_float_value(self):
        attrs = OrderFactory.attributes()
        attrs['value'] = 100.
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_bad_user(self):
        attrs = OrderFactory.attributes()
        attrs['user'] = 'abc'
        self.assertRaises(ValueError, order.Order, **attrs)

    def test_good(self):
        attrs = OrderFactory.attributes()
        self.assertTrue(order.Order(**attrs))
