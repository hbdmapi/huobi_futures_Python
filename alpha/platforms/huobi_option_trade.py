# -*- coding:utf-8 -*-

"""
Huobi Option Api Module.

Author: QiaoXiaofeng
Date:   2020/06/19
Email:  andyjoe318@gmail.com
"""

import gzip
import json
import copy
import datetime
import time
import urllib
import hmac
import base64
import urllib
import hashlib
import datetime
import time
from urllib.parse import urljoin

from alpha.asset import Asset
from alpha.order import Order
from alpha.position import Position
from alpha.error import Error
from alpha.utils import tools, logger
from alpha.tasks import SingleTask, LoopRunTask
from alpha.const import HUOBI_OPTION
from alpha.utils.websocket import Websocket
from alpha.utils.request import AsyncHttpRequests
from alpha.utils.decorator import async_method_locker
from alpha.order import ORDER_ACTION_BUY, ORDER_ACTION_SELL
from alpha.order import ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET, ORDER_TYPE_MAKER, ORDER_TYPE_FOK, ORDER_TYPE_IOC
from alpha.order import ORDER_STATUS_SUBMITTED, ORDER_STATUS_PARTIAL_FILLED, ORDER_STATUS_FILLED, \
    ORDER_STATUS_CANCELED, ORDER_STATUS_FAILED, TRADE_TYPE_BUY_OPEN, TRADE_TYPE_SELL_OPEN, TRADE_TYPE_BUY_CLOSE, \
    TRADE_TYPE_SELL_CLOSE
from .huobi_option_api import HuobiOptionRestAPI


__all__ = ("HuobiOptionTrade", )
    
class HuobiOptionTrade(Websocket):
    """ Huobi Option Trade module. You can initialize trade object with some attributes in kwargs.

    Attributes:
        account: Account name for this trade exchange.
        strategy: What's name would you want to created for you strategy.
        symbol: Symbol name for your trade.
        host: HTTP request host. default `https://api.hbdm.com"`.
        wss: Websocket address. default `wss://api.hbdm.com`.
        access_key: Account's ACCESS KEY.
        secret_key Account's SECRET KEY.
        asset_update_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `asset_update_callback` is like `async def on_asset_update_callback(asset: Asset): pass` and this
            callback function will be executed asynchronous when received AssetEvent.
        order_update_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `order_update_callback` is like `async def on_order_update_callback(order: Order): pass` and this
            callback function will be executed asynchronous when some order state updated.
        position_update_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `position_update_callback` is like `async def on_position_update_callback(order: Position): pass` and
            this callback function will be executed asynchronous when some position state updated.
        init_success_callback: You can use this param to specific a async callback function when you initializing Trade
            object. `init_success_callback` is like `async def on_init_success_callback(success: bool, error: Error, **kwargs): pass`
            and this callback function will be executed asynchronous after Trade module object initialized successfully.
    """

    def __init__(self, **kwargs):
        """Initialize."""
        e = None
        if not kwargs.get("account"):
            e = Error("param account miss")
        if not kwargs.get("strategy"):
            e = Error("param strategy miss")
        if not kwargs.get("symbol"):
            e = Error("param symbol miss")
        if not kwargs.get("host"):
            kwargs["host"] = "https://api.hbdm.com"
        if not kwargs.get("wss"):
            kwargs["wss"] = "wss://api.hbdm.com"
        if not kwargs.get("access_key"):
            e = Error("param access_key miss")
        if not kwargs.get("secret_key"):
            e = Error("param secret_key miss")
        if e:
            logger.error(e, caller=self)
            if kwargs.get("init_success_callback"):
                SingleTask.run(kwargs["init_success_callback"], False, e)
            return

        self._account = kwargs["account"]
        self._strategy = kwargs["strategy"]
        self._platform = HUOBI_OPTION
        self._symbol = kwargs["symbol"]
        self._host = kwargs["host"]
        self._wss = kwargs["wss"]
        self._access_key = kwargs["access_key"]
        self._secret_key = kwargs["secret_key"]
        self._order_update_callback = kwargs.get("order_update_callback")
        self._position_update_callback = kwargs.get("position_update_callback")
        self._asset_update_callback = kwargs.get("asset_update_callback")
        self._init_success_callback = kwargs.get("init_success_callback")

        url = self._wss + "/option-notification"
        super(HuobiOptionTrade, self).__init__(url, send_hb_interval=5)

        self._raw_symbol = self._symbol.split("-")[0]
        self._trade_partition = self._symbol.split("-")[1]

        self._assets = {}  # Asset detail, {"BTC": {"free": "1.1", "locked": "2.2", "total": "3.3"}, ... }.
        self._orders = {}  # Order objects, {"order_id": order, ...}.
        self._position = Position(self._platform, self._account, self._strategy, self._symbol)

        self._order_channel = "orders.{symbol}".format(symbol='-'.join(self._symbol.split('-')[:2]))
        self._position_channel = "positions.{symbol}".format(symbol='-'.join(self._symbol.split('-')[:2]))
        self._asset_channels = ["accounts.{symbol}".format(symbol='-'.join(self._symbol.split('-')[:2])),
                                "accounts.{symbol}".format(symbol='-'.join([self._symbol.split('-')[1], self._symbol.split('-')[1]]))]


        self._subscribe_order_ok = False
        self._subscribe_position_ok = False
        self._subscribe_asset_ok = False

        self._rest_api = HuobiOptionRestAPI(self._host, self._access_key, self._secret_key)

        self.initialize()


    @property
    def assets(self):
        return copy.copy(self._assets)

    @property
    def orders(self):
        return copy.copy(self._orders)

    @property
    def position(self):
        return copy.copy(self._position)

    @property
    def rest_api(self):
        return self._rest_api

    async def _send_heartbeat_msg(self, *args, **kwargs):
        data = {"pong": int(time.time()*1000)}
        if not self.ws:
            logger.error("Websocket connection not yeah!", caller=self)
            return
        await self.ws.send_json(data)

    async def connected_callback(self):
        """After connect to Websocket server successfully, send a auth message to server."""
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        data = {
            "AccessKeyId": self._access_key,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": "2",
            "Timestamp": timestamp
        }
        sign = self.generate_signature("GET", data, "/option-notification")
        data["op"] = "auth"
        data["type"] = "api"
        data["Signature"] = sign
        await self.ws.send_json(data)
    
    def generate_signature(self, method, params, request_path):
        host_url = urllib.parse.urlparse(self._wss).hostname.lower()
        #host_url = "172.18.6.227:9090"
        sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = "\n".join(payload)
        payload = payload.encode(encoding="UTF8")
        secret_key = self._secret_key.encode(encoding="utf8")
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    async def auth_callback(self, data):
        if data["err-code"] != 0:
            e = Error("Websocket connection authorized failed: {}".format(data))
            logger.error(e, caller=self)
            SingleTask.run(self._init_success_callback, False, e)
            return

        # subscribe order
        data = {
            "op": "sub",
            "cid": tools.get_uuid1(),
            "topic": self._order_channel
        }
        await self.ws.send_json(data)

        # subscribe position
        data = {
            "op": "sub",
            "cid": tools.get_uuid1(),
            "topic": self._position_channel
        }
        await self.ws.send_json(data)

        # subscribe asset
        for channel in self._asset_channels:
            data = {
                "op": "sub",
                "cid": tools.get_uuid1(),
                "topic": channel
            }
            await self.ws.send_json(data)

    async def sub_callback(self, data):
        if data["err-code"] != 0:
            e = Error("subscribe {} failed!".format(data["topic"]))
            logger.error(e, caller=self)
            SingleTask.run(self._init_success_callback, False, e)
            return
        if data["topic"] == self._order_channel:
            self._subscribe_order_ok = True
        elif data["topic"] == self._position_channel:
            self._subscribe_position_ok = True
        elif data["topic"] in self._asset_channels:
            self._subscribe_asset_ok = True
        if self._subscribe_order_ok and self._subscribe_position_ok \
            and self._subscribe_asset_ok:
            success, error = await self._rest_api.get_open_orders(self._symbol)
            if error:
                e = Error("get open orders failed!")
                SingleTask.run(self._init_success_callback, False, e)
            elif "data" in success and "orders" in success["data"]:
                for order_info in success["data"]["orders"]:
                    order_info["ts"] = order_info["created_at"]
                    self._update_order(order_info)
                SingleTask.run(self._init_success_callback, True, None)
            else:
                logger.warn("get open orders:", success, caller=self)
                e = Error("Get Open Orders Unknown error")
                SingleTask.run(self._init_success_callback, False, e)

    @async_method_locker("HuobiOptionTrade.process_binary.locker")
    async def process_binary(self, raw):
        """ 处理websocket上接收到的消息
        @param raw 原始的压缩数据
        """
        data = json.loads(gzip.decompress(raw).decode())
        logger.debug("data:", data, caller=self)

        op = data.get("op")
        if op == "ping":
            hb_msg = {"op": "pong", "ts": int(data.get("ts"))}
            await self.ws.send_json(hb_msg)

        elif op == "auth":
            await self.auth_callback(data)

        elif op == "sub":
            await self.sub_callback(data)

        elif op == "notify":
            if data["topic"].startswith("orders"):
                self._update_order(data)
            elif data["topic"].startswith("positions"):
                self._update_position(data)
            elif data["topic"].startswith("accounts"):
                self._update_asset(data)

    async def create_order(self, action, price, quantity, order_type=ORDER_TYPE_LIMIT, *args, **kwargs):
        """ Create an order.

        Args:
            action: Trade direction, BUY or SELL.
            price: Price of each contract.
            quantity: The buying or selling quantity.
            order_type: Order type, LIMIT or MARKET.
            kwargs:
                lever_rate: Leverage rate, 10 or 20.

        Returns:
            order_no: Order ID if created successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        if int(quantity) > 0:
            if action == ORDER_ACTION_BUY:
                direction = "buy"
                offset = "open"
            elif action == ORDER_ACTION_SELL:
                direction = "sell"
                offset = "close"
            else:
                return None, "action error"
        else:
            if action == ORDER_ACTION_BUY:
                direction = "buy"
                offset = "close"
            elif action == ORDER_ACTION_SELL:
                direction = "sell"
                offset = "open"
            else:
                return None, "action error"

        if order_type == ORDER_TYPE_LIMIT:
            order_price_type = "limit"
        elif order_type == ORDER_TYPE_MARKET:
            order_price_type = "optimal_20"
        elif order_type == ORDER_TYPE_MAKER:
            order_price_type = "post_only"
        elif order_type == ORDER_TYPE_FOK:
            order_price_type = "fok"
        elif order_type == ORDER_TYPE_IOC:
            order_price_type = "ioc"

        else:
            return None, "order type error"

        quantity = abs(int(quantity))
        result, error = await self._rest_api.create_order(self._symbol,
                                                          price, quantity, direction, offset,
                                                          order_price_type)
        if error:
            return None, error
        return str(result["data"]["order_id"]), None
    
    async def create_orders(self, orders, *args, **kwargs):
        """ batch create orders
        
        Args:
            orders_data: [] 
            list item:
                action: Trade direction, BUY or SELL.
                price: Price of each contract.
                quantity: The buying or selling quantity.
                order_type: Order type, LIMIT or MARKET.
            kwargs:
                
        Returns:
            success: order info  if created successfully.
            error: erros information.
        """
        orders_data = []
        for order in orders:
            if int(order["quantity"]) > 0:
                if order["action"] == ORDER_ACTION_BUY:
                    direction = "buy"
                    offset = "open"
                elif order["action"] == ORDER_ACTION_SELL:
                    direction = "sell"
                    offset = "close"
                else:
                    return None, "action error"
            else:
                if order["action"] == ORDER_ACTION_BUY:
                    direction = "buy"
                    offset = "close"
                elif order["action"] == ORDER_ACTION_SELL:
                    direction = "sell"
                    offset = "open"
                else:
                    return None, "action error"

            if order["order_type"] == ORDER_TYPE_LIMIT:
                order_price_type = "limit"
            elif order["order_type"] == ORDER_TYPE_MARKET:
                order_price_type = "optimal_20"
            elif order["order_type"] == ORDER_TYPE_MAKER:
                order_price_type = "post_only"
            elif  order["order_type"] == ORDER_TYPE_FOK:
                order_price_type = "fok"
            elif  order["order_type"] == ORDER_TYPE_IOC:
               order_price_type = "ioc"
            else:
                return None, "order type error"

            quantity = abs(int(order["quantity"]))

            client_order_id = order.get("client_order_id", "")

            orders_data.append({"contract_code": self._symbol, \
                    "client_order_id": client_order_id, "price": order["price"], "volume": quantity, "direction": direction, "offset": offset, \
                    "order_price_type":  order_price_type})

        result, error = await self._rest_api.create_orders({"orders_data": orders_data})
        if error:
            return None, error
        order_nos = [ order["order_id"] for order in result.get("data").get("success")]
        return order_nos, result.get("data").get("errors")
        
    async def revoke_order(self, *order_nos):
        """ Revoke (an) order(s).

        Args:
            order_nos: Order id list, you can set this param to 0 or multiple items. If you set 0 param, you can cancel
                all orders for this symbol(initialized in Trade object). If you set 1 param, you can cancel an order.
                If you set multiple param, you can cancel multiple orders. Do not set param length more than 100.

        Returns:
            Success or error, see bellow.
        """
        # If len(order_nos) == 0, you will cancel all orders for this symbol(initialized in Trade object).
        if len(order_nos) == 0:
            success, error = await self._rest_api.revoke_order_all(self._raw_symbol, self._trade_partition, "", self._symbol)
            if error:
                return False, error
            if success.get("errors"):
                return False, success["errors"]
            return True, None

        # If len(order_nos) == 1, you will cancel an order.
        if len(order_nos) == 1:
            success, error = await self._rest_api.revoke_order(self._trade_partition, order_nos[0])
            if error:
                return order_nos[0], error
            if success.get("errors"):
                return False, success["errors"]
            else:
                return order_nos[0], None

        # If len(order_nos) > 1, you will cancel multiple orders.
        if len(order_nos) > 1:
            success, error = await self._rest_api.revoke_orders(self._trade_partition, order_nos)
            if error:
                return order_nos[0], error
            if success.get("errors"):
                return False, success["errors"]
            return success, error

    async def get_open_order_nos(self):
        """ Get open order id list.

        Args:
            None.

        Returns:
            order_nos: Open order id list, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        success, error = await self._rest_api.get_open_orders("","",self._symbol)
        if error:
            return None, error
        else:
            order_nos = []
            for order_info in success["data"]["orders"]:
                if order_info["contract_code"] != self._symbol:
                    continue
                order_nos.append(str(order_info["order_id"]))
            return order_nos, None

    def _update_order(self, order_info):
        """ Order update.

        Args:
            order_info: Order information.
        """
        if order_info["contract_code"] != self._symbol:
            return
        order_no = str(order_info["order_id"])
        status = order_info["status"]

        order = self._orders.get(order_no)
        if not order:
            if order_info["direction"] == "buy":
                if order_info["offset"] == "open":
                    trade_type = TRADE_TYPE_BUY_OPEN
                else:
                    trade_type = TRADE_TYPE_BUY_CLOSE
            else:
                if order_info["offset"] == "close":
                    trade_type = TRADE_TYPE_SELL_CLOSE
                else:
                    trade_type = TRADE_TYPE_SELL_OPEN

            info = {
                "platform": self._platform,
                "account": self._account,
                "strategy": self._strategy,
                "order_no": order_no,
                "action": ORDER_ACTION_BUY if order_info["direction"] == "buy" else ORDER_ACTION_SELL,
                "symbol": self._symbol,
                "price": order_info["price"],
                "quantity": order_info["volume"],
                "trade_type": trade_type
            }
            order = Order(**info)
            self._orders[order_no] = order

        if status in [1, 2, 3]:
            order.status = ORDER_STATUS_SUBMITTED
        elif status == 4:
            order.status = ORDER_STATUS_PARTIAL_FILLED
            order.remain = int(order.quantity) - int(order_info["trade_volume"])
        elif status == 6:
            order.status = ORDER_STATUS_FILLED
            order.remain = 0
        elif status in [5, 7]:
            order.status = ORDER_STATUS_CANCELED
            order.remain = int(order.quantity) - int(order_info["trade_volume"])
        else:
            return

        order.avg_price = order_info["trade_avg_price"]
        order.ctime = order_info["created_at"]
        order.utime = order_info["ts"]

        SingleTask.run(self._order_update_callback, copy.copy(order))

        # Delete order that already completed.
        if order.status in [ORDER_STATUS_FAILED, ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED]:
            self._orders.pop(order_no)
        
        # publish order
        logger.info("symbol:", order.symbol, "order:", order, caller=self)

    def _update_position(self, data):
        """ Position update.

        Args:
            position_info: Position information.

        Returns:
            None.
        """
        for position_info in data["data"]:
            if position_info["contract_code"] != self._symbol:
                continue
            if position_info["direction"] == "buy":
                self._position.long_quantity = int(position_info["volume"])
                self._position.long_avg_price = position_info["cost_hold"]
            else:
                self._position.short_quantity = int(position_info["volume"])
                self._position.short_avg_price = position_info["cost_hold"]
            # self._position.liquid_price = None
            self._position.utime = data["ts"]
            SingleTask.run(self._position_update_callback, copy.copy(self._position))
    
    def _update_asset(self, data):
        """ Asset update.

        Args:
            data: asset data.
        
        Returns:
            None.
        """
        assets = {}
        for item in data["data"]:
            symbol = item["symbol"].upper()
            total = float(item["margin_balance"])
            free = float(item["margin_available"])
            locked = float(item["margin_frozen"])
            premium_frozen = float(item.get("premium_frozen")) if item.get("premium_frozen") else 0.0
            premium_in = float(item.get("premium_in")) if item.get("premium_in") else 0.0
            premium_out = float(item.get("premium_out")) if item.get("premium_out") else 0.0
            delta = float(item.get("delta")) if item.get("delta") else 0.0
            gamma = float(item.get("gamma")) if item.get("gamma") else 0.0
            theta = float(item.get("theta")) if item.get("theta") else 0.0
            vega = float(item.get("vega")) if item.get("vega") else 0.0
            option_value = float(item.get("option_value")) if item.get("option_value") else 0.0
            if total > 0:
                assets[symbol] = {
                    "total": "%.8f" % total,
                    "free": "%.8f" % free,
                    "locked": "%.8f" % locked,
                    "premium_frozen": "%.8f" % premium_frozen,
                    "premium_in": "%.8f" % premium_in,
                    "premium_out": "%.8f" % premium_out,
                    "delta": "%.8f" % delta,
                    "gamma": "%.8f" % gamma,
                    "theta": "%.8f" % theta,
                    "vega": "%.8f" % vega,
                    "option_value": "%.8f" % option_value
                }
        if assets == self._assets:
            update = False
        else:
            update = True
        
        if hasattr(self._assets, "assets") is False:
            info = {
                "platform": self._platform,
                "account": self._account,
                "assets": assets,
                "timestamp": tools.get_cur_timestamp_ms(),
                "update": update
            }
            asset = Asset(**info)
            self._assets = asset
            SingleTask.run(self._asset_update_callback, copy.copy(self._assets))
        else:
            for symbol in assets:
                self._assets.assets.update({
                    symbol: assets[symbol]
                    })
            self._assets.timestamp = tools.get_cur_timestamp_ms()
            SingleTask.run(self._asset_update_callback, copy.copy(self._assets))
