from decimal import Decimal as D
import uuid

import factory

from pytrade import order


class OrderFactory(factory.Factory):
    FACTORY_FOR = order.Order

    type = order.BUY
    amount = D(100)
    value = D(10000)
    user = uuid.uuid4()
