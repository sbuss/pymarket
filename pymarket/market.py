import logging
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from Queue import Empty

from order import BUY
from order import SELL
from orderbook import PriorityOrderBook
from utils import format_int_value


logger = logging.getLogger('pymarket.market')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class Market(Process):
    def __init__(self, buy_book, sell_book, order_queue):
        self.buy_book = buy_book
        self.sell_book = sell_book
        self.order_queue = order_queue
        super(Market, self).__init__()

    def add_orders_to_books(self):
        while not self.order_queue.empty():
            try:
                order = self.order_queue.get_nowait()
            except Empty:
                return
            else:
                logger.info("Received %s" % order)
                if order.type == BUY:
                    self.buy_book.add(order)
                elif order.type == SELL:
                    self.sell_book.add(order)

    def run(self):
        """Match open Buys with Sells."""
        logger.info("Market open for business")
        logger.info(self.order_queue)
        logger.info(self.order_queue.empty())
        while True:
            self.add_orders_to_books()  # First flush the order queue
            self.match_orders()

    def match_orders(self):
        info_msg = "Bought {quantity} at ${purchase_price} for ${total}"
        top_buy = self.buy_book.peek()
        top_sell = self.sell_book.peek()
        if not (top_buy and top_sell):
            return

        if top_buy.value >= top_sell.value:
            logger.info("Top buy: %s" % top_buy)
            logger.info("Top sell: %s" % top_sell)
            top_buy = self.buy_book.pop()
            top_sell = self.sell_book.pop()

            purchase_price = top_sell.value
            quantity = top_sell.amount
            if top_buy.amount > top_sell.amount:
                top_buy.amount -= top_sell.amount
                self.order_queue.put(top_buy)
            elif top_buy.amount < top_sell.amount:
                top_sell.amount -= top_buy.amount
                self.order_queue.put(top_sell)
                quantity = top_buy.amount
            logger.info(info_msg.format(
                quantity=quantity,
                purchase_price=format_int_value(purchase_price),
                total=format_int_value(quantity * purchase_price)))


class MarketManager(BaseManager):
    pass


order_queue = Queue()
MarketManager.register('get_order_queue', lambda: order_queue)


if __name__ == "__main__":
    logger.info("Starting server")
    market = Market(PriorityOrderBook(BUY), PriorityOrderBook(SELL),
                    order_queue)
    market.start()
    manager = MarketManager(address=('localhost', 5555), authkey='pymarket')
    server = manager.get_server()
    server.serve_forever()
