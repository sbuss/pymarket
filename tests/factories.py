import uuid

import factory

from pymarket import order


class OrderFactory(factory.Factory):
    FACTORY_FOR = order.Order

    type = order.BUY
    amount = 100
    value = 10000
    user = uuid.uuid4()
