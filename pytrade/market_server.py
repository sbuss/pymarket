import logging
from multiprocessing import Queue
from multiprocessing.managers import BaseManager

logger = logging.getLogger('pytrade.market')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class MarketManager(BaseManager):
    pass


order_queue = Queue()
MarketManager.register('get_order_queue', lambda: order_queue)


if __name__ == "__main__":
    logger.info("Starting server")
    manager = MarketManager(address=('localhost', 5555), authkey='pymarket')
    server = manager.get_server()
    server.serve_forever()
