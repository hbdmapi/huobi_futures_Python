# -*— coding:utf-8 -*-

"""
Huobi USDT Swap Market Server.

Author: Qiaoxiaofeng
Date:   2020/9/10
Email:  andyjoe318@gmail.com
"""

import gzip
import json
import time
import asyncio
import copy
from collections import deque

from alpha.utils import logger
from alpha.utils.websocket import Websocket
from alpha.utils.decorator import async_method_locker
from alpha.const import MARKET_TYPE_KLINE
from alpha.order import ORDER_ACTION_BUY, ORDER_ACTION_SELL
from alpha.tasks import SingleTask
from alpha.orderbook import Orderbook
from alpha.markettrade import Trade
from alpha.kline import Kline

class HuobiUsdtSwapMarket(Websocket):
    """ Huobi USDT Swap Market Server.

    Attributes:
        kwargs:
            platform: Exchange platform name, must be `huobi_usdt_swap`.
            wss: Exchange Websocket host address.
            symbols: Trade pair list, e.g. ["BTC_USDT"].
            channels: channel list, only `orderbook`, `kline` and `trade` to be enabled.
            orderbook_length: The length of orderbook's data to be published via OrderbookEvent, default is 10.
    """

    def __init__(self, **kwargs):
        self._platform = kwargs["platform"]
        self._wss = kwargs.get("wss", "wss://api.hbdm.com")
        self._symbols = list(set(kwargs.get("symbols")))
        self._channels = kwargs.get("channels")
        self._orderbook_length = kwargs.get("orderbook_length", 10)
        self._orderbooks_length = kwargs.get("orderbooks_length", 100)
        self._klines_length = kwargs.get("klines_length", 100)
        self._trades_length = kwargs.get("trades_length", 100)
        self._orderbook_update_callback = kwargs.get("orderbook_update_callback")
        self._kline_update_callback = kwargs.get("kline_update_callback")
        self._trade_update_callback = kwargs.get("trade_update_callback")

        self._c_to_s = {}  # {"channel": "symbol"}
        self._orderbooks = deque(maxlen=self._orderbooks_length) 
        self._klines = deque(maxlen=self._klines_length)
        self._trades = deque(maxlen=self._trades_length)

        url = self._wss + "/linear-swap-ws"
        super(HuobiUsdtSwapMarket, self).__init__(url, send_hb_interval=5)
        self.initialize()
    
    @property
    def orderbooks(self):
        return copy.copy(self._orderbooks)

    @property
    def klines(self):
        return copy.copy(self._klines)

    @property
    def trades(self):
        return copy.copy(self._trades)

    async def _send_heartbeat_msg(self, *args, **kwargs):
        """ 发送心跳给服务器
        """
        if not self.ws:
            logger.warn("websocket connection not connected yet!", caller=self)
            return
        data = {"pong": int(time.time()*1000)}
        try:
            await self.ws.send_json(data)
        except ConnectionResetError:
            await asyncio.get_event_loop().create_task(self._reconnect())

    async def connected_callback(self):
        """ After create Websocket connection successfully, we will subscribing orderbook/trade events.
        """
        for ch in self._channels:
            if ch == "kline":
                for symbol in self._symbols:
                    channel = self._symbol_to_channel(symbol, "kline")
                    if not channel:
                        continue
                    kline = {
                        "sub": channel
                    }
                    await self.ws.send_json(kline)
            elif ch == "orderbook":
                for symbol in self._symbols:
                    channel = self._symbol_to_channel(symbol, "depth")
                    if not channel:
                        continue
                    data = {
                        "sub": channel
                    }
                    await self.ws.send_json(data)
            elif ch == "trade":
                for symbol in self._symbols:
                    channel = self._symbol_to_channel(symbol, "trade")
                    if not channel:
                        continue
                    data = {
                        "sub": channel
                    }
                    await self.ws.send_json(data)
            else:
                logger.error("channel error! channel:", ch, caller=self)

    async def process_binary(self, msg):
        """ Process binary message that received from Websocket connection.
        """
        data = json.loads(gzip.decompress(msg).decode())
        logger.debug("data:", json.dumps(data), caller=self)
        channel = data.get("ch")
        if not channel:
            if data.get("ping"):
                hb_msg = {"pong": data.get("ping")}
                await self.ws.send_json(hb_msg)
            return

        symbol = self._c_to_s[channel]

        if channel.find("kline") != -1:
            await self.process_kline(data)

        elif channel.find("depth") != -1:
            await self.process_orderbook(data)
        
        elif channel.find("trade") != -1:
            await self.process_trade(data)
        else:
            logger.error("event error! msg:", msg, caller=self)

    def _symbol_to_channel(self, symbol, channel_type):
        """ Convert symbol to channel.

        Args:
            symbol: Trade pair name.such as BTC-USD
            channel_type: channel name, kline / ticker / depth.
        """
        if channel_type == "kline":
            channel = "market.{s}.kline.1min".format(s=symbol.upper())
        elif channel_type == "depth":
            channel = "market.{s}.depth.step6".format(s=symbol.upper())
        elif channel_type == "trade":
            channel = "market.{s}.trade.detail".format(s=symbol.upper())
        else:
            logger.error("channel type error! channel type:", channel_type, caller=self)
            return None
        self._c_to_s[channel] = symbol
        return channel
    
    async def process_kline(self, data):
        """ process kline data
        """
        channel = data.get("ch")
        symbol = self._c_to_s[channel]
        d = data.get("tick")
        info = {
            "platform": self._platform,
            "symbol": symbol,
            "open": "%.8f" % d["open"],
            "high": "%.8f" % d["high"],
            "low": "%.8f" % d["low"],
            "close": "%.8f" % d["close"],
            "volume": "%.8f" % d["amount"],
            "timestamp": int(data.get("ts")),
            "kline_type": MARKET_TYPE_KLINE
        }
        kline = Kline(**info)
        self._klines.append(kline)
        SingleTask.run(self._kline_update_callback, copy.copy(kline))

        logger.debug("symbol:", symbol, "kline:", kline, caller=self)

    async def process_orderbook(self, data):
        """ process orderbook data
        """
        channel = data.get("ch")
        symbol = self._c_to_s[channel]
        d = data.get("tick")
        asks, bids = [], []
        if d.get("asks"):
            for item in d.get("asks")[:self._orderbook_length]:
                price = "%.8f" % item[0]
                quantity = "%.8f" % item[1]
                asks.append([price, quantity])
        if d.get("bids"):
            for item in d.get("bids")[:self._orderbook_length]:
                price = "%.8f" % item[0]
                quantity = "%.8f" % item[1]
                bids.append([price, quantity])
        info = {
            "platform": self._platform,
            "symbol": symbol,
            "asks": asks,
            "bids": bids,
            "timestamp": d.get("ts")
        }
        orderbook = Orderbook(**info)
        self._orderbooks.append(orderbook)
        SingleTask.run(self._orderbook_update_callback, copy.copy(orderbook))
        logger.debug("symbol:", symbol, "orderbook:", orderbook, caller=self)
    
    async def process_trade(self, data):
        """ process trade
        """
        channel = data.get("ch")
        symbol = self._c_to_s[channel]
        ticks = data.get("tick")
        for tick in ticks["data"]: 
            direction = tick.get("direction")
            price = tick.get("price")
            quantity = tick.get("amount")
            info = {
                "platform": self._platform,
                "symbol": symbol,
                "action": ORDER_ACTION_BUY if direction == "buy" else ORDER_ACTION_SELL,
                "price": "%.8f" % price,
                "quantity": "%.8f" % quantity,
                "timestamp": tick.get("ts")
            }
            trade = Trade(**info)
            self._trades.append(trade)
            SingleTask.run(self._trade_update_callback, copy.copy(trade))
            logger.debug("symbol:", symbol, "trade:", trade, caller=self)
        



