import logging

logger = logging.getLogger('pytrade.market')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class Market(object):
    def __init__(self, buy_book, sell_book):
        self.buy_book = buy_book
        self.sell_book = sell_book

    def match(self):
        """Match open Buys with Sells."""
        while True:
            top_buy = self.buy_book.peek()
            top_sell = self.sell_book.peek()
            if top_buy.value >= top_sell.value:
                logger.info("Top buy: %s" % top_buy)
                logger.info("Top sell: %s" % top_sell)
                top_buy = self.buy_book.pop()
                top_sell = self.sell_book.pop()
                if top_buy.amount > top_sell.amount:
                    top_buy.amount -= top_sell.amount
                    self.buy_book.add(top_buy)
                    logger.info("Bought %s for $%s",
                                top_sell.amount, top_sell.value)
                elif top_buy.amount < top_sell.amount:
                    top_sell.amount -= top_buy.amount
                    self.sell_book.add(top_sell)
                    logger.info("Bought %s for $%s",
                                top_buy.amount, top_sell.value)
                else:
                    logger.info("Bought %s for $%s",
                                top_buy.amount, top_sell.value)
