# -*- coding:utf-8 -*-

"""
Market Module.

Author: QiaoXiaofeng
Date:   2020/01/10
Email:  andyjoe318@gmail.com
"""

import copy

from alpha import const
from alpha.utils import logger
from alpha.tasks import SingleTask
from alpha.orderbook import Orderbook
from alpha.kline import Kline
from alpha.markettrade import Trade


class Market:
    """ Market Module.

    Attributes:
        platform: Exchange platform name. e.g. `huobi_swap`.
        symbols: Symbol name for your trade. e.g. [`BTC-USD`]
        channels: sub channels.e.g.['kline', 'orderbook', 'trade']
        orderbook_length: max orderbook length.default 10.
        wss: Websocket address.
        orderbook_update_callback: You can use this param to specific a async callback function when you initializing Market
            object. `orderbook_update_callback` is like `async def on_orderbook_update_callback(orderbook: Orderbook): pass` and this
            callback function will be executed asynchronous when received AssetEvent.
        kline_update_callback: You can use this param to specific a async callback function when you initializing Market
            object. `kline_update_callback` is like `async def on_kline_update_callback(kline: Kline): pass` and this
            callback function will be executed asynchronous when some order state updated.
        trade_update_callback: You can use this param to specific a async callback function when you initializing
            Market object. `trade_update_callback` is like `async def on_trade_update_callback(trade: Trade): pass`
            and this callback function will be executed asynchronous when trade updated.
    """

    def __init__(self, platform=None, symbols=None, channels=None, orderbook_length=None, orderbooks_length=None,\
                klines_length=None, trades_length=None, wss=None, \
                orderbook_update_callback=None, kline_update_callback=None, trade_update_callback=None, **kwargs):
        """initialize trade object."""
        kwargs["platform"] = platform
        kwargs["symbols"] = symbols
        kwargs["channels"] = channels
        kwargs["orderbook_length"] = orderbook_length
        kwargs["orderbooks_length"] = orderbooks_length
        kwargs["klines_length"] = klines_length
        kwargs["trades_length"] = trades_length
        kwargs["wss"] = wss
        kwargs["orderbook_update_callback"] = orderbook_update_callback
        kwargs["kline_update_callback"] = kline_update_callback
        kwargs["trade_update_callback"] = trade_update_callback

        self._raw_params = copy.copy(kwargs)
        self._on_orderbook_update_callback = orderbook_update_callback
        self._on_kline_update_callback = kline_update_callback
        self._on_trade_update_callback = trade_update_callback

        if platform == const.HUOBI_SWAP:
            from alpha.platforms.huobi_swap_market import HuobiSwapMarket  as M
        else:
            logger.error("platform error:", platform, caller=self)
            return
        self._m = M(**kwargs)

    @property
    def orderbooks(self):
        return self._m.orderbooks

    @property
    def klines(self):
        return self._m.klines

    @property
    def trades(self):
        return self._m.trades