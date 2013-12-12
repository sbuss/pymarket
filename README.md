# PyMarket

PyMarket is a simple stock market engine, allowing a single stock to be traded.
Only limit orders are currently supported.


# Running

```python
python -m pymarket.market
```

This runs the market as a server which you can connect to. In order to send
buys and sells you must connect to the order queue:

```python
import uuid
from pymarket.market import MarketManager
from pymarket.order import Buy
from pymarket.order import Sell
from pymarket.order import Order
from pymarket.order import CancelOrder

market = MarketManager(address=('localhost', 5555), authkey='pymarket')
market.connect()
order_queue = market.get_order_queue()

order_queue.put(Order(BUY, 100, 100, uuid.uuid4()))
order_queue.put(Order(SELL, 10, 100, uuid.uuid4()))
order_queue.put(Order(SELL, 10, 95, uuid.uuid4()))
order_queue.put(Order(SELL, 100, 90, uuid.uuid4()))
order = Order(BUY, 100, 80, uuid.uuid4()))
order_queue.put(order)
order_queue.put(CancelOrder(order.id))
```
