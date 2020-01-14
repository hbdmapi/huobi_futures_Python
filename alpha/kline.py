# -*- coding:utf-8 -*-

"""
Market module.

Author: QiaoXiaofeng
Date:   2020/1/10
Email:  andyjoe318@gmail.com
"""

import json

from alpha import const
from alpha.utils import logger


class Orderbook:
    """ Orderbook object.

    Args:
        platform: Exchange platform name, e.g. huobi_swap.
        symbol: Trade pair name, e.g. BTC-USD.
        asks: Asks list, e.g. [[price, quantity], [...], ...]
        bids: Bids list, e.g. [[price, quantity], [...], ...]
        timestamp: Update time, millisecond.
    """

    def __init__(self, platform=None, symbol=None, asks=None, bids=None, timestamp=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.asks = asks
        self.bids = bids
        self.timestamp = timestamp

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "asks": self.asks,
            "bids": self.bids,
            "timestamp": self.timestamp
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)


class Trade:
    """ Trade object.

    Args:
        platform: Exchange platform name, e.g. huobi_swap.
        symbol: Trade pair name, e.g. BTC-USD.
        action: Trade action, BUY or SELL.
        price: Order place price.
        quantity: Order place quantity.
        timestamp: Update time, millisecond.
    """

    def __init__(self, platform=None, symbol=None, action=None, price=None, quantity=None, timestamp=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.action = action
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "action": self.action,
            "price": self.price,
            "quantity": self.quantity,
            "timestamp": self.timestamp
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)


class Kline:
    """ Kline object.

    Args:
        platform: Exchange platform name, e.g. huobi_swap.
        symbol: Trade pair name, e.g. BTC-USD.
        open: Open price.
        high: Highest price.
        low: Lowest price.
        close: Close price.
        volume: Total trade volume.
        timestamp: Update time, millisecond.
        kline_type: Kline type name, kline - 1min, kline_5min - 5min, kline_15min - 15min.
    """

    def __init__(self, platform=None, symbol=None, open=None, high=None, low=None, close=None, volume=None,
                 timestamp=None, kline_type=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = timestamp
        self.kline_type = kline_type

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "timestamp": self.timestamp,
            "kline_type": self.kline_type
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)