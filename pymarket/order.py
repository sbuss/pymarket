from collections import namedtuple
import uuid

BUY = 'buy'
SELL = 'sell'


class Order(object):
    def __init__(self, type, amount, value, user):
        if type != BUY and type != SELL:
            raise ValueError("type must be one of %s" % ([BUY, SELL],))
        if amount < 1 or not isinstance(amount, int):
            raise ValueError("Amount must be a positive integer")
        if value < 1 or not isinstance(value, int):
            raise ValueError("Value must be a positive integer")
        if not isinstance(user, uuid.UUID):
            raise ValueError("Users must be identified by their UUIDs")

        self.id = uuid.uuid4()
        self.type = type
        self.amount = amount
        self.value = value
        self.user = user

    def __lt__(self, other):
        """
        A BUY is less than another BUY if its value is GREATER.
        A SELL is less than another SELL if its value is LESSER.

        This weird construct is because we want to be able to efficiently
        find the buys & sells that overlap in order to make the market,
        which means matching the "smallest" buy with the smallest sell.

            Buy@20 < Buy@10
            Sell@20 < Sell@30

        We can thus implement an OrderBook as a simple ordering of available
        Buy and Sell orders and only have to look at the few smallest Orders,
        which can typically be done quite efficiently.
        """
        if self.type == BUY:
            return self.value > other.value
        else:
            return self.value < other.value

    def __eq__(self, other):
        return (self.id == other.id and
                self.type == other.type and
                self.amount == other.amount and
                self.value == other.value and
                self.user == other.user)

    def __repr__(self):
        return "Order<%s>(%s, %s, $%s, %s)" % (
            self.id, self.type, self.amount, self.value, self.user)


CancelOrder = namedtuple('CancelOrder', [
    'order_id'])
