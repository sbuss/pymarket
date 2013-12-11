from decimal import Decimal

TWO_PLACES = Decimal(10) ** -2


def format_int_value(value):
    return "%s" % (Decimal(value) / 100).quantize(TWO_PLACES)
