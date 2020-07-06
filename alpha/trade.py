# -*- coding:utf-8 -*-

"""
Trade Module.

Author: QiaoXiaofeng
Date:   2019/04/21
Email:  andyjoe318@gmail.com
"""

import copy

from alpha import const
from alpha.error import Error
from alpha.utils import logger
from alpha.tasks import SingleTask
from alpha.order import ORDER_TYPE_LIMIT
from alpha.order import Order
from alpha.position import Position


class Trade:
    """ Trade Module.

    Attributes:
        strategy: What's name would you want to created for your strategy.
        platform: Exchange platform name. e.g. `huobi_swap`.
        symbol: Symbol name for your trade. e.g. `BTC-USD`.
        host: HTTP request host.
        wss: Websocket address.
        account: Account name for this trade exchange.
        access_key: Account's ACCESS KEY.
        secret_key: Account's SECRET KEY.
        asset_update_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `asset_update_callback` is like `async def on_asset_update_callback(asset: Asset): pass` and this
            callback function will be executed asynchronous when received AssetEvent.
        order_update_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `order_update_callback` is like `async def on_order_update_callback(order: Order): pass` and this
            callback function will be executed asynchronous when some order state updated.
        position_update_callback: You can use this param to specific a async callback function when you initializing
            Trade object. `position_update_callback` is like `async def on_position_update_callback(position: Position): pass`
            and this callback function will be executed asynchronous when position updated.
        init_success_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `init_success_callback` is like `async def on_init_success_callback(success: bool, error: Error, **kwargs): pass`
            and this callback function will be executed asynchronous after Trade module object initialized successfully.
    """

    def __init__(self, strategy=None, platform=None, symbol=None, host=None, wss=None, account=None, access_key=None,
                 secret_key=None, asset_update_callback=None, order_update_callback=None,
                 position_update_callback=None, init_success_callback=None, **kwargs):
        """initialize trade object."""
        kwargs["strategy"] = strategy
        kwargs["platform"] = platform
        kwargs["symbol"] = symbol
        kwargs["host"] = host
        kwargs["wss"] = wss
        kwargs["account"] = account
        kwargs["access_key"] = access_key
        kwargs["secret_key"] = secret_key
        kwargs["asset_update_callback"] = asset_update_callback
        kwargs["order_update_callback"] = self._on_order_update_callback
        kwargs["position_update_callback"] = self._on_position_update_callback
        kwargs["init_success_callback"] = self._on_init_success_callback

        self._raw_params = copy.copy(kwargs)
        self._order_update_callback = order_update_callback
        self._position_update_callback = position_update_callback
        self._init_success_callback = init_success_callback

        if platform == const.HUOBI_SWAP:
            from alpha.platforms.huobi_swap_trade import HuobiSwapTrade as T
        elif platform == const.HUOBI_FUTURE:
            from alpha.platforms.huobi_future_trade import HuobiFutureTrade as T
        elif platform == const.HUOBI_OPTION:
            from alpha.platforms.huobi_option_trade import HuobiOptionTrade as T
        else:
            logger.error("platform error:", platform, caller=self)
            e = Error("platform error")
            SingleTask.run(self._init_success_callback, False, e)
            return
        kwargs.pop("platform")
        self._t = T(**kwargs)

    @property
    def assets(self):
        return self._t.assets

    @property
    def orders(self):
        return self._t.orders

    @property
    def position(self):
        return self._t.position

    @property
    def rest_api(self):
        return self._t.rest_api

    async def create_order(self, action, price, quantity, order_type=ORDER_TYPE_LIMIT, **kwargs):
        """ Create an order.

        Args:
            action: Trade direction, `BUY` or `SELL`.
            price: Price of each contract.
            quantity: The buying or selling quantity.
            order_type: Specific type of order, `LIMIT` or `MARKET`. (default is `LIMIT`)

        Returns:
            order_no: Order ID if created successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        order_no, error = await self._t.create_order(action, price, quantity, order_type, **kwargs)
        return order_no, error
    
    async def create_orders(self, orders_data, **kwargs):
        """ Create batch order

        Returns:
            orders_no:
            error: error information.
        """
        order_nos, error = await self._t.create_orders(orders_data, **kwargs)
        return order_nos, error


    async def revoke_order(self, *order_nos):
        """ Revoke (an) order(s).

        Args:
            order_nos: Order id list, you can set this param to 0 or multiple items. If you set 0 param, you can cancel
                all orders for this symbol(initialized in Trade object). If you set 1 param, you can cancel an order.
                If you set multiple param, you can cancel multiple orders. Do not set param length more than 100.

        Returns:
            success: If execute successfully, return success information, otherwise it's None.
            error: If execute failed, return error information, otherwise it's None.
        """
        success, error = await self._t.revoke_order(*order_nos)
        return success, error

    async def get_open_order_nos(self):
        """ Get open order id list.

        Args:
            None.

        Returns:
            order_nos: Open order id list, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        result, error = await self._t.get_open_order_nos()
        return result, error

    async def _on_order_update_callback(self, order: Order):
        """ Order information update callback.

        Args:
            order: Order object.
        """
        if self._order_update_callback:
            SingleTask.run(self._order_update_callback, order)

    async def _on_position_update_callback(self, position: Position):
        """ Position information update callback.

        Args:
            position: Position object.
        """
        if self._position_update_callback:
            SingleTask.run(self._position_update_callback, position)

    async def _on_init_success_callback(self, success: bool, error: Error):
        """ Callback function when initialize Trade module finished.

        Args:
            success: `True` if initialize Trade module success, otherwise `False`.
            error: `Error object` if initialize Trade module failed, otherwise `None`.
        """
        if self._init_success_callback:
            params = {
                "strategy": self._raw_params["strategy"],
                "platform": self._raw_params["platform"],
                "symbol": self._raw_params["symbol"],
                "account": self._raw_params["account"]
            }
            await self._init_success_callback(success, error, **params)
