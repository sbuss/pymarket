import unittest

from pytrade import order
from tests.factories import OrderFactory


class TestOrderCreation(unittest.TestCase):
    def test_bad_type(self):
        attrs = OrderFactory.attributes()
        attrs['type'] = 'abc'
        self.assertRaises(ValueError, order.Order, *attrs)
