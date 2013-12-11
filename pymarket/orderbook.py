import heapq

from order import BUY
from order import SELL


class OrderBook(object):
    def __init__(self, type, orders=None):
        """Construct an OrderBook of type book_type.

        This base class uses a naive sorted list to maintain the list of
        orders.

        Args:
            type: Either order.BUY or order.SELL
            orders: An optional list of Orders to start the book with.
        """
        if type != BUY and type != SELL:
            raise ValueError("type must be one of %s" % ([BUY, SELL],))
        self.type = type

        if orders:
            for order in orders:
                self.add(order)

    def _add(self, order):
        raise NotImplementedError()

    def _pop(self):
        raise NotImplementedError()

    def _peek(self):
        raise NotImplementedError()

    def _cancel(self, order):
        raise NotImplementedError()

    def has_orders(self):
        raise NotImplementedError()

    def add(self, order):
        """Add an Order to the order book."""
        if order.type != self.type:
            raise ValueError("Order type (%s) does not match book type (%s)" %
                             (order.type, self.type))
        self._add(order)

    def pop(self):
        """Remove the top Order from the order book.

        For Buy order books, the top Order is the one with the highest bid
        price, for Sell order books, the top Order is the one with the lowest
        offer price.
        """
        if self.has_orders():
            return self._pop()
        return None

    def peek(self):
        """View the current top Order in the order book."""
        if self.has_orders():
            return self._peek()
        return None

    def cancel(self, order_id):
        """Cancel the given Order.

        Args:
            order_id: The ID of the Order to cancel. This does not take an
                Order instance because it may have been partially filled and
                wouldn't equal the Order passed in.

        Returns True if the order was cancelled, False if it couldn't be
        found.
        """
        return self._cancel(order_id)


class ListOrderBook(OrderBook):
    def __init__(self, *args, **kwargs):
        self.orders = []
        super(ListOrderBook, self).__init__(*args, **kwargs)

    def _add(self, order):
        self.orders.append(order)
        self.orders = sorted(self.orders)

    def _pop(self):
        return self.orders.pop(0)

    def _peek(self):
        return self.orders[0]

    def _cancel(self, order_id):
        for i, order in enumerate(self.orders):
            if order.id == order_id:
                del self.orders[i]
                return

    def has_orders(self):
        return len(self.orders) > 0


class PriorityOrderBook(ListOrderBook):
    def _add(self, order):
        heapq.heappush(self.orders, order)

    def _pop(self):
        return heapq.heappop(self.orders)

    def _peek(self):
        return self.orders[0]

    def _cancel(self, order_id):
        super(PriorityOrderBook, self)._cancel(order_id)
        heapq.heapify(self.orders)
