# -*- coding:utf-8 -*-

"""
Huobi Option Api Module.

Author: QiaoXiaofeng
Date:   2020/06/24
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


__all__ = ("HuobiOptionRestAPI", )

class HuobiOptionRestAPI:
    """ Huobi Option REST API Client.

    Attributes:
        host: HTTP request host.
        access_key: Account's ACCESS KEY.
        secret_key: Account's SECRET KEY.
        passphrase: API KEY Passphrase.
    """

    def __init__(self, host, access_key, secret_key):
        """ initialize REST API client. """
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key

    async def get_option_info(self, contract_code=None):
        """ Get Option Info
        
        Args:
            symbol: option.such as "BTC"
            trade_partition: option. such as "USDT"
            contract_type: option. such as "this_week","next_week","quarter"
            contract_code:  option. such as "BTC-USDT-200508-C-8800".
        
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        * Note: 1. If input `contract_code`, only matching this contract code.
                2. If not input 'contract_code', matching all contract_codes.
        """
        uri = "/option-api/v1/option_contract_info"
        params = {}
        if contract_code:
            params["contract_code"] = contract_code
        success, error = await self.request("GET", uri, params)
        return success, error

    async def get_price_limit(self, contract_code):
        """ Get swap price limit.

        Args:
            contract_code:  such as "BTC-USDT-200508-C-8800".

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        * NOTE: 1. If input `contract_code`, only matching this contract code.
                2. If not input 'contract_code', matching all contract_codes.
        """
        uri = "/option-api/v1/option_price_limit"
        params = {}
        params["contract_code"] = contract_code
        success, error = await self.request("GET", uri, params=params)
        return success, error

    async def get_market_index(self, contract_code):
        """ Get Market Index

        Args:
            contract_code: such as BTC-USDT-200508-C-8800
        
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None. 

        """
        uri = "/option-api/v1/option_market_index"
        params = {}
        params["contract_code"] = contract_code
        success, error = await self.request("GET", uri, params=params)
        return success, error

    async def get_orderbook(self, contract_code):
        """ Get orderbook information.

        Args:
            contract_code:  such as "TC-USDT-200508-C-8800".

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-ex/market/depth"
        params = {
            "contract_code": contract_code,
            "type": "step0"
        }
        success, error = await self.request("GET", uri, params=params)
        return success, error

    async def get_asset_info(self, symbol=None, trade_partition=None):
        """ Get account asset information.

        Args:
            symbol: such as "BTC".
            trade_partition: such as "USDT". 

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_account_info"
        body = {}
        if symbol:
            body["symbol"] = symbol
        if trade_partition:
            body["trade_partition"] = trade_partition
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_position(self, symbol=None, trade_partition=None,contract_code=None):
        """ Get position information.

        Args:
            symbol: such as "BTC".
            trade_partition: such as "USDT".
            contract_code: such as "BTC-USDT-200508-C-8800".

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_position_info"
        body = {}
        if symbol:
            body["symbol"] = symbol
        if trade_partition:
            body["trade_partition"] = trade_partition
        if contract_code:
            body["contract_code"] = contract_code
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def create_order(self, contract_code, price, quantity, direction, offset,
                           order_price_type, client_order_id=None):
        """ Create an new order.

        Args:
            contract_code: such as "BTC-USDT-200508-C-8800".
            price: Order price.
            quantity: Order amount.
            direction: Transaction direction, `buy` / `sell`.
            offset: `open` / `close`.
            order_price_type: Order type, `limit` - limit order, `opponent` - market order.etc.
            client_order_id: long. 

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_order"
        body = {
            "contract_code": contract_code,
            "price": price,
            "volume": quantity,
            "direction": direction,
            "offset": offset,
            "order_price_type": order_price_type
        }
        if client_order_id:
            body.update({"client_order_id": client_order_id})
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def create_orders(self, orders_data):
        """ Batch Create orders.
            orders_data = {'orders_data': [
               {  
                'contract_code':'BTC-USDT-200508-C-8800',  'client_order_id':'', 
                'price':1, 'volume':1, 'direction':'buy', 'offset':'open', 
                'order_price_type':'limit'},
               { 
                'contract_code':'BTC-USDT-200508-C-8800', 'client_order_id':'', 
                'price':2, 'volume':2, 'direction':'buy', 'offset':'open', 
                'order_price_type':'limit'}]}   
        """
        uri = "/option-api/v1/option_batchorder"
        body = orders_data
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
        

    async def revoke_order(self, trade_partition="", order_id="", client_order_id=""):
        """ Revoke an order.

        Args:
            trade_partition: trade partition such as "USDT".
            order_id: Order ID.
            client_order_id: client order.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_cancel"
        body = {
            "trade_partition": trade_partition,
            "order_id": order_id,
            "client_order_id": client_order_id
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def revoke_orders(self, trade_partition="", order_ids=[], client_order_ids=[]):
        """ Revoke multiple orders.

        Args:
            trade_partition: trade partition such as "USDT".
            order_ids: Order ID list.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_cancel"
        body = {
            "trade_partition": trade_partition,
            "order_id": ",".join(order_ids),
            "client_order_id": ",".join(client_order_ids)
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def revoke_order_all(self, trade_partition="", contract_type="", contract_code=""):
        """ Revoke all orders.

        Args:
            trade_partition: such as "USDT".
            contract_type: such as "this_week", "next_week", "quarter".
            contract_code: such as "BTC-USDT-200508-C-8800".


        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        """
        uri = "/option-api/v1/option_cancelall"
        body = {
            "trade_partition": trade_partition,
            "contract_type": contract_type,
            "contract_code": contract_code
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_order_info(self, symbol, trade_partition="", order_ids=[], client_order_ids=[]):
        """ Get order information.

        Args:
            symbol: such as "BTC".
            trade_partition: such as "USDT".
            contract_code: such as "BTC-USDT-200508-C-8800".
            order_ids: Order ID list. (different IDs are separated by ",", maximum 50 orders can be requested at one time.)
            client_order_ids: Client Order ID list. (different IDs are separated by ",", maximum 50 orders can be requested at one time.)

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_order_info"
        body = {
            "symbol": symbol,
            "trade_partition": trade_partition,
            "order_id": ",".join(order_ids),
            "client_order_id": ",".join(client_order_ids)
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def get_open_orders(self, contract_code="", symbol="", trade_partition="",  index=1, size=50):
        """ Get open order information.

        Args:
            symbol: such as "BTC".
            trade_partition: such as "USDT".
            contract_code: such as "BTC-USDT-200508-C-8800".
            index: Page index, default 1st page.
            size: Page size, Default 20，no more than 50.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/option-api/v1/option_openorders"
        body = {
            "symbol": symbol,
            "trade_partition": trade_partition,
            "contract_code": contract_code,
            "page_index": index,
            "page_size": size
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error
    
    async def get_history_orders(self, symbol,  trade_type, stype, status, \
        create_date, trade_partition="", contract_code="", order_type="", page_index=0, page_size=50):
        """ Get history orders information.

        Args:
            symbol: such as "BTC".
            trade_partition: such as "USDT".
            contract_code: such as "BTC-USDT-200508-C-8800".
            trade_type: 0:all,1: buy long,2: sell short,3: buy short,4: sell long,5: sell liquidation,6: buy liquidation,7:Delivery long,8: Delivery short
            stype: 1:All Orders,2:Order in Finished Status
            status: status: 1. Ready to submit the orders; 2. Ready to submit the orders; 3. Have sumbmitted the orders; \
                4. Orders partially matched; 5. Orders cancelled with partially matched; 6. Orders fully matched; 7. Orders cancelled; 11. Orders cancelling.
            create_date: any positive integer available. Requesting data beyond 90 will not be supported, otherwise, system will return trigger history data \
                within the last 90 days by default.
            page_index: default 1st page
            page_size: default page size 20. 50 max.
        
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.

        """
        uri = "/option-api/v1/option_hisorders"
        body = {
            "symbol": symbol,
            "trade_partition": trade_partition,
            "contract_code": contract_code,
            "trade_type": trade_type,
            "type": stype,
            "order_type": order_type,
            "status": status,
            "create_date": create_date,
            "page_index": page_index,
            "page_size": page_size
        }
        success, error = await self.request("POST", uri, body=body, auth=True)
        return success, error

    async def transfer_between_spot_option(self,  symbol, amount, from_, to, tradePartition="USDT"):
        """ Do transfer between spot and option.
        Args:
            symbol: currency,such as btc,eth,etc.
            amount: transfer amount.pls note the precision digit is 8.
            from_: 'spot' or 'option'
            to: 'spot' or 'option',
            tradePartition: trade partition.
            
        """
        body = {
                "currency": symbol,
                "amount": amount,
                "from": from_,
                "to": to,
                "tradePartition": tradePartition
                }

        uri = "https://api.huobi.pro/v2/account/transfer"
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
        if uri.startswith("http://") or uri.startswith("https://"):
            url = uri
        else:
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
        if request_path.startswith("http://") or request_path.startswith("https://"):
            host_url = urllib.parse.urlparse(request_path).hostname.lower()
            request_path = '/' + '/'.join(request_path.split('/')[3:])
        else:
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
