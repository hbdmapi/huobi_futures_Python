# -*- coding:utf-8 -*-
"""
简单卖平策略，仅做演示使用

Author: QiaoXiaofeng
Date:   2020/12/28
Email: andyjoe318@gmail.com
"""
# 策略实现
import time
from alpha import const
from alpha.utils import tools
from alpha.utils import logger
from alpha.utils import mongo
from alpha.config import config
from alpha.market import Market
from alpha.trade import Trade
from alpha.order import Order
from alpha.orderbook import Orderbook
from alpha.kline import Kline
from alpha.markettrade import Trade as MarketTrade
from alpha.asset import Asset
from alpha.position import Position
from alpha.error import Error
from alpha.tasks import LoopRunTask
from alpha.order import ORDER_ACTION_SELL, ORDER_ACTION_BUY, ORDER_STATUS_FAILED, ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED,\
    ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET


class MyStrategy:

    def __init__(self):
        """ 初始化
        """
        self.strategy = config.strategy
        self.symbol = config.symbol
        self.contract_type = config.contract_type
        self.channels = config.markets[0]["channels"]
        self.orderbook_length = config.markets[0]["orderbook_length"]
        self.orderbooks_length = config.markets[0]["orderbooks_length"]
        self.klines_length = config.markets[0]["klines_length"]
        self.trades_length = config.markets[0]["trades_length"]
        self.market_wss = config.markets[0]["wss"]
        self.platform = config.markets[0]["platform"]

        # 行情模块
        cc = {
            "platform": self.platform,
            "symbols": [self.symbol],
            "channels": self.channels,
            "orderbook_length": self.orderbook_length,
            "orderbooks_length": self.orderbooks_length,
            "klines_length": self.klines_length,
            "trades_length": self.trades_length,
            "wss": self.market_wss,
            "orderbook_update_callback": self.on_event_orderbook_update,
            "kline_update_callback": self.on_event_kline_update,
            "trade_update_callback": self.on_event_trade_update
        }
        self.market = Market(**cc)
                
    async def on_event_orderbook_update(self, orderbook: Orderbook):
        """  orderbook更新
            self.market.orderbooks 是最新的orderbook组成的队列，记录的是历史N次orderbook的数据。
            本回调所传的orderbook是最新的单次orderbook。
        """
        logger.debug("orderbook:", orderbook, caller=self)
        if orderbook.asks:
            self.ask1_price = float(orderbook.asks[0][0])  # 卖一价格
            self.ask1_volume = float(orderbook.asks[0][1])  # 卖一数量
        if orderbook.bids:
            self.bid1_price = float(orderbook.bids[0][0])  # 买一价格
            self.bid1_volume = float(orderbook.bids[0][1])  # 买一数量
        self.last_orderbook_timestamp = orderbook.timestamp

    async def on_event_order_update(self, order: Order):
        """ 订单状态更新
        """
        logger.info("order update:", order, caller=self)

    async def on_event_asset_update(self, asset: Asset):
        """ 资产更新
        """
        logger.info("asset update:", asset, caller=self)

    async def on_event_position_update(self, position: Position):
        """ 仓位更新
        """
        logger.info("position update:", position, caller=self)
    
    async def on_event_kline_update(self, kline: Kline):
        """ kline更新
            self.market.klines 是最新的kline组成的队列，记录的是历史N次kline的数据。
            本回调所传的kline是最新的单次kline。
        """
        logger.debug("kline update:", kline, caller=self)
        result = await mongo.MongoDBBase('quant', 'kline').find_one_and_update({'platform': kline.platform, 'symbol': kline.symbol, \
            'timestamp': kline.timestamp, 'kline_type': kline.kline_type}, {'$set': {'open': kline.open, 'high': kline.high, \
            'close': kline.close, 'low': kline.low, 'volume': kline.volume }}, upsert=True, return_document=True)
        if not result:
            logger.error("insert mongo error ", kline.platform+kline.symbol, kline, result)
        logger.debug("insert mongo success: ", result)
    
    async def on_event_trade_update(self, trade: MarketTrade):
        """ market trade更新
            self.market.trades 是最新的逐笔成交组成的队列，记录的是历史N次trade的数据。
            本回调所传的trade是最新的单次trade。
        """
        logger.debug("trade update:", trade, caller=self)
    
    async def on_event_init_success_callback(self, success: bool, error: Error, **kwargs):
        """ init success callback
        """
        logger.debug("init success callback update:", success, error, kwargs, caller=self)

