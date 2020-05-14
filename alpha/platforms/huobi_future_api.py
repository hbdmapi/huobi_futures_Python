# -*- coding:utf-8 -*-

"""
Huobi Future Api Module.

Author: QiaoXiaofeng
Date:   2020/02/10
Email:  andyjoe318@gmail.com
"""

import gzip
import json
import copy
import hmac
import base64
import urllib
import hashlib
import datetime
import time
from urllib.parse import urljoin
from alpha.utils.request import AsyncHttpRequests
from alpha.const import USER_AGENT


__all__ = ("HuobiFutureRestAPI", )

class HuobiFutureRestAPI:
    """ Huobi Swap REST API client.

    Attributes:
        host: HTTP request host.
        access_key: Account's ACCESS KEY.
        secret_key: Account's SECRET KEY.
        passphrase: API KEY Passphrase.
    """

    def __init__(self, host, access_key, secret_key):
        """initialize REST API client."""
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key

    async def get_contract_info(self, symbol=None, contract_type=None, contract_code=None):
        """ Get contract information.

        Args:
            symbol: Trade pair, default `None` will return all symbols.
            contract_type: Contract type, `this_week` / `next_week` / `quarter`, default `None` will return all types.
            contract_code: Contract code, e.g. BTC180914.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        * NOTE: 1. If input `contract_code`, only matching this contract code.
                2. If not input `contract_code`, matching by `symbol + contract_type`.
        """
        uri = "/api/v1/contract_contract_info"
        params = {}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params["contract_type"] = contract_type
        if contract_code:
            params["contract_code"] = contract_code
        success, error = await self.request("GET", uri, params)
        return success, error

    async def get_price_limit(self, symbol=None, contract_type=None, contract_code=None):
        """ Get contract price limit.

        Args:
            symbol: Trade pair, default `None` will return all symbols.
            contract_type: Contract type, `this_week` / `next_week` / `quarter`, default `None` will return all types.
            contract_code: Contract code, e.g. BTC180914.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        * NOTE: 1. If input `contract_code`, only matching this contract code.
                2. If not input `contract_code`, matching by `symbol + contract_type`.
        """
        uri = "/api/v1/contract_price_limit"
        params = {}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params["contract_type"] = contract_type
        if contract_code:
            params["contract_code"] = contract_code
        success, error = await self.request("GET", uri, params=params)
        return success, error

    async def get_orderbook(self, symbol):
        """ Get orderbook information.

        Args:
            symbol: Symbol name, `BTC_CW` - current week, `BTC_NW` next week, `BTC_CQ` current quarter.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/market/depth"
        params = {
            "symbol": symbol,
            "type": "step0"
        }
        success, error = await self.request("GET", uri, params=params)
        return success, error

    async def get_asset_info(self):
        """ Get account asset information.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_account_info"
        success, error = await self.request("POST", uri, auth=True)
        return success, error

    async def get_position(self, symbol=None):
        """ Get position information.

        Args:
            symbol: Currency name, e.g. BTC. default `None` will return all types.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_position_info"
        body = {}
        if symbol:
            body["symbol"] = symbol
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_order_info(self, symbol, order_ids=[], client_order_ids=[]):
        """ Get order information.

        Args:
            contract_code: such as "BTC".
            order_ids: Order ID list. (different IDs are separated by ",", maximum 20 orders can be requested at one time.)
            client_order_ids: Client Order ID list. (different IDs are separated by ",", maximum 20 orders can be requested at one time.)

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_order_info"
        body = {
            "symbol": symbol,
            "order_id": ",".join(order_ids),
            "client_order_id": ",".join(client_order_ids)
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def create_order(self, symbol, contract_type, contract_code, price, quantity, direction, offset, lever_rate,
                           order_price_type):
        """ Create an new order.

        Args:
            symbol: Currency name, e.g. BTC.
            contract_type: Contract type, `this_week` / `next_week` / `quarter`.
            contract_code: Contract code, e.g. BTC180914.
            price: Order price.
            quantity: Order amount.
            direction: Transaction direction, `buy` / `sell`.
            offset: `open` / `close`.
            lever_rate: Leverage rate, 10 or 20.
            order_price_type: Order type, `limit` - limit order, `opponent` - market order.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_order"
        body = {
            "symbol": symbol,
            "contract_type": contract_type,
            "contract_code": contract_code,
            "price": price,
            "volume": quantity,
            "direction": direction,
            "offset": offset,
            "lever_rate": lever_rate,
            "order_price_type": order_price_type
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def create_orders(self, orders_data):
        """ Batch Create orders.
            orders_data = {'orders_data': [
               {'symbol': 'BTC', 'contract_type': 'quarter',  
                'contract_code':'BTC181228',  'client_order_id':'', 
                'price':1, 'volume':1, 'direction':'buy', 'offset':'open', 
                'leverRate':20, 'orderPriceType':'limit'},
               {'symbol': 'BTC','contract_type': 'quarter', 
                'contract_code':'BTC181228', 'client_order_id':'', 
                'price':2, 'volume':2, 'direction':'buy', 'offset':'open', 
                'leverRate':20, 'orderPriceType':'limit'}]}   
        """
        uri = "/api/v1/contract_batchorder"
        body = orders_data
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
        

    async def revoke_order(self, symbol, order_id):
        """ Revoke an order.

        Args:
            symbol: Currency name, e.g. BTC.
            order_id: Order ID.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_cancel"
        body = {
            "symbol": symbol,
            "order_id": order_id
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def revoke_orders(self, symbol, order_ids):
        """ Revoke multiple orders.

        Args:
            symbol: Currency name, e.g. BTC.
            order_ids: Order ID list.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_cancel"
        body = {
            "symbol": symbol,
            "order_id": ",".join(order_ids)
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def revoke_order_all(self, symbol, contract_code=None, contract_type=None):
        """ Revoke all orders.

        Args:
            symbol: Currency name, e.g. BTC.
            contract_type: Contract type, `this_week` / `next_week` / `quarter`, default `None` will return all types.
            contract_code: Contract code, e.g. BTC180914.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        * NOTE: 1. If input `contract_code`, only matching this contract code.
                2. If not input `contract_code`, matching by `symbol + contract_type`.
        """
        uri = "/api/v1/contract_cancelall"
        body = {
            "symbol": symbol,
        }
        if contract_code:
            body["contract_code"] = contract_code
        if contract_type:
            body["contract_type"] = contract_type
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_order_info(self, symbol, order_ids):
        """ Get order information.

        Args:
            symbol: Currency name, e.g. BTC.
            order_ids: Order ID list. (different IDs are separated by ",", maximum 20 orders can be withdrew at one time.)

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_order_info"
        body = {
            "symbol": symbol,
            "order_id": ",".join(order_ids)
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_open_orders(self, symbol, index=1, size=50):
        """ Get open order information.

        Args:
            symbol: Currency name, e.g. BTC.
            index: Page index, default 1st page.
            size: Page size, Default 20，no more than 50.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/api/v1/contract_openorders"
        body = {
            "symbol": symbol,
            "page_index": index,
            "page_size": size
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def get_api_trading_status(self):
        """ Get api trading status.
        Args:
            None.
        Returns:
            refer to https://huobiapi.github.io/docs/dm/v1/cn/#api-5
        """
        uri = "/api/v1/contract_api_trading_status"
        success, error = await self.request("GET", uri, body=None, auth=True)
        return success, error

    async def create_trigger_order(self, symbol, contract_type, trigger_type, \
        trigger_price, order_price, order_price_type, volume, direction, offset, lever_rate, contract_code=None):
        """ Create trigger order

        Args:
            symbol: symbol,such as BTC.
            contract_type: contract type,such as this_week,next_week,quarter
            contract_code: contract code,such as BTC190903. If filled,the above symbol and contract_type will be ignored.
            trigger_type: trigger type,such as ge,le.
            trigger_price: trigger price.
            order_price: order price.
            order_price_type: "limit" by default."optimal_5"\"optimal_10"\"optimal_20"
            volume: volume.
            direction: "buy" or "sell".
            offset: "open" or "close".
            lever_rate: lever rate.
        
        Returns:
            refer to https://huobiapi.github.io/docs/dm/v1/cn/#97a9bd626d

        """
        uri = "/api/v1/contract_trigger_order"
        body = {
            "symbol": symbol,
            "contract_type": contract_type,
            "trigger_type": trigger_type,
            "trigger_price": trigger_price,
            "order_price": order_price,
            "order_price_type": order_price_type,
            "volume": volume,
            "direction": direction,
            "offset": offset,
            "lever_rate": lever_rate
        }
        if contract_code:
            body.update({"contract_code": contract_code})

        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def revoke_trigger_order(self, symbol, order_id):
        """ Revoke trigger order

        Args: 
            symbol: symbol,such as "BTC".
            order_id: order ids.multiple orders need to be joined by ','.

        Returns:
            refer to https://huobiapi.github.io/docs/dm/v1/cn/#0d42beab34

        """
        uri = "/api/v1/contract_trigger_cancel"
        body = {
            "symbol": symbol,
            "order_id": order_id
        }
        
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def revoke_all_trigger_orders(self, symbol, contract_code=None, contract_type=None):
        """ Revoke all trigger orders

        Args:
            symbol: symbol, such as "BTC"
            contract_code: contract_code, such as BTC180914.
            contract_type: contract_type, such as this_week, next_week, quarter.
        
        Returns:
            refer to https://huobiapi.github.io/docs/dm/v1/cn/#3d2471d520

        """
        uri = "/api/v1/contract_trigger_cancelall"
        body = {
            "symbol": symbol
        }
        if contract_code:
            body.update({"contract_code": contract_code})
        if contract_type:
            body.update({"contract_type": contract_type})

        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def get_trigger_openorders(self, symbol, contract_code=None, page_index=None, page_size=None):
        """ Get trigger openorders
        Args: 
            symbol: symbol, such as "BTC"
            contract_code: contract code, such as BTC180914.
            page_index: page index.1 by default.
            page_size: page size.20 by default.
        
        Returns: 
            refer to https://huobiapi.github.io/docs/dm/v1/cn/#b5280a27b3
        """

        uri = "/api/v1/contract_trigger_openorders"
        body = {
            "symbol": symbol,
        }
        if contract_code:
            body.update({"contract_code": contract_code})
        if page_index:
            body.update({"page_index": page_index})
        if page_size:
            body.update({"page_size": page_size})
        
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def get_trigger_hisorders(self, symbol, trade_type, status, create_date, contract_code=None, page_index=None, page_size=None):
        """ Get trigger hisorders
        
        Args:
            symbol: symbol,such as "BTC"
            contract_code: contract code.
            trade_type: trade type. 0:all 1:open buy 2:open sell 3:close buy 4:close sell
            status: status. 0: orders finished. 4: orders submitted. 5: order filled. 6:order cancelled. multiple status is joined by ','
            create_date: days. such as 1-90.
            page_index: 1 by default.
            page_size: 20 by default.50 at most.

        Returns:
            https://huobiapi.github.io/docs/dm/v1/cn/#37aeb9f3bd

        """

        uri = "/api/v1/contract_trigger_hisorders"
        body = {
            "symbol": symbol,
            "trade_type": trade_type,
            "status": status,
            "create_date": create_date,
        }
        if contract_code:
            body.update({"contract_code": contract_code})
        if page_index:
            body.update({"page_index": page_index})
        if page_size:
            body.update({"page_size": page_size})
        
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def request(self, method, uri, params=None, body=None, headers=None, auth=False):
        """ Do HTTP request.

        Args:
            method: HTTP request method. `GET` / `POST` / `DELETE` / `PUT`.
            uri: HTTP request uri.
            params: HTTP query params.
            body: HTTP request body.
            headers: HTTP request headers.
            auth: If this request requires authentication.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        url = urljoin(self._host, uri)

        if auth:
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            params = params if params else {}
            params.update({"AccessKeyId": self._access_key,
                           "SignatureMethod": "HmacSHA256",
                           "SignatureVersion": "2",
                           "Timestamp": timestamp})

            params["Signature"] = self.generate_signature(method, params, uri)

        if not headers:
            headers = {}
        if method == "GET":
            headers["Content-type"] = "application/x-www-form-urlencoded"
            headers["User-Agent"] = USER_AGENT
            _, success, error = await AsyncHttpRequests.fetch("GET", url, params=params, headers=headers, timeout=10)
        else:
            headers["Accept"] = "application/json"
            headers["Content-type"] = "application/json"
            headers["User-Agent"] = USER_AGENT
            _, success, error = await AsyncHttpRequests.fetch("POST", url, params=params, data=body, headers=headers,
                                                              timeout=10)
        if error:
            return None, error
        if not isinstance(success, dict):
            result = json.loads(success)
        else:
            result = success
        if result.get("status") != "ok":
            return None, result
        return result, None

    def generate_signature(self, method, params, request_path):
        host_url = urllib.parse.urlparse(self._host).hostname.lower()
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