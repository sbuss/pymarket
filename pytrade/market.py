import logging
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.managers import BaseManager

from order import BUY
from order import SELL
from orderbook import PriorityOrderBook


logger = logging.getLogger('pytrade.market')
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
            except:
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
            self.add_orders_to_books()
            top_buy = self.buy_book.peek()
            top_sell = self.sell_book.peek()
            if not (top_buy and top_sell):
                continue
            if top_buy.value >= top_sell.value:
                logger.info("Top buy: %s" % top_buy)
                logger.info("Top sell: %s" % top_sell)
                top_buy = self.buy_book.pop()
                top_sell = self.sell_book.pop()
                if top_buy.amount > top_sell.amount:
                    top_buy.amount -= top_sell.amount
                    self.order_queue.put(top_buy)
                    logger.info("Bought %s at $%s for $%s",
                                top_sell.amount, top_sell.value,
                                top_sell.amount * top_sell.value)
                elif top_buy.amount < top_sell.amount:
                    top_sell.amount -= top_buy.amount
                    self.order_queue.put(top_sell)
                    logger.info("Bought %s at $%s for $%s",
                                top_buy.amount, top_sell.value,
                                top_buy.amount * top_sell.value)
                else:
                    logger.info("Bought %s at $%s for $%s",
                                top_buy.amount, top_sell.value,
                                top_buy.amount * top_sell.value)


class MarketManager(BaseManager):
    pass


order_queue = Queue()
MarketManager.register('get_order_queue', lambda: order_queue)


if __name__ == "__main__":
    logger.info("Starting server")
    market = Market(PriorityOrderBook(BUY), PriorityOrderBook(SELL),
                    order_queue)
    market.start()
    manager = MarketManager(address=('localhost', 5555), authkey='pytrade')
    server = manager.get_server()
    server.serve_forever()
