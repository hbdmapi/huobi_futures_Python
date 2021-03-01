import websocket
import threading

import gzip
import json
from datetime import datetime
from urllib import parse
import hmac
import base64
from hashlib import sha256
from alpha.platforms.huobi_usdt_swap.logger import *
import time


class WsUtils:
    def __init__(self, path: str, host: str = None, access_key: str = None, secret_key: str = None):
        self._path = path
        if host is None:
            host = "api.btcgateway.pro"
        self._host = host
        url = 'wss://{}{}'.format(host, path)
        logger.info(url)
        self._ws = websocket.WebSocketApp(url,
                                          on_open=self._on_open,
                                          on_message=self._on_msg,
                                          on_close=self._on_close,
                                          on_error=self._on_error)
        self._worker = threading.Thread(target=self._ws.run_forever)
        self._worker.start()

        self._has_open = False
        self._auth = True
        self._access_key = access_key
        self._secret_key = secret_key
        if access_key is not None or secret_key is not None:
            self._auth = False

        self._sub_map = {}
        self._req_map = {}

    def __del__(self):
        self.close()

    def _send_auth_data(self, method: str, path: str, host: str, access_key: str, secret_key: str):
        # timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        # get Signature
        suffix = 'AccessKeyId={}&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp={}'.format(
            access_key, parse.quote(timestamp))
        payload = '{}\n{}\n{}\n{}'.format(method.upper(), host, path, suffix)

        digest = hmac.new(secret_key.encode('utf8'), payload.encode(
            'utf8'), digestmod=sha256).digest()
        signature = base64.b64encode(digest).decode()

        # data
        data = {
            "op": "auth",
            "type": "api",
            "AccessKeyId": access_key,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": "2",
            "Timestamp": timestamp,
            "Signature": signature
        }
        data = json.dumps(data)
        self._ws.send(data)
        logger.info(data)

    def _on_open(self):
        logger.info('ws open.')
        if self._auth == False:
            self._send_auth_data('get', self._path, self._host,
                                 self._access_key, self._secret_key)
        self._has_open = True

    def _handle_notify(self, opdata: str, jdata, plain:str):
        key = jdata['topic']
        key = key.lower()
        if key in self._sub_map:
            callback = self._sub_map[key]
            callback(jdata)
        elif key.startswith('orders_cross') and 'orders_cross.*' in self._sub_map:
            callback = self._sub_map['orders_cross.*']
            callback(jdata)
        elif key.startswith('orders') and 'orders.*' in self._sub_map:
            callback = self._sub_map['orders.*']
            callback(jdata)
        elif key.startswith('accounts_cross') and 'accounts_cross.*' in self._sub_map:
            callback = self._sub_map['accounts_cross.*']
            callback(jdata)
        elif key.startswith('accounts') and 'accounts.*' in self._sub_map:
            callback = self._sub_map['accounts.*']
            callback(jdata)
        elif key.startswith('positions_cross') and 'positions_cross.*' in self._sub_map:
            callback = self._sub_map['positions_cross.*']
            callback(jdata)
        elif key.startswith('positions') and 'positions.*' in self._sub_map:
            callback = self._sub_map['positions.*']
            callback(jdata)
        elif key.startswith('matchorders_cross') and 'matchorders_cross.*' in self._sub_map:
            callback = self._sub_map['matchOrders_cross.*']
            callback(jdata)
        elif key.startswith('matchorders') and 'matchorders.*' in self._sub_map:
            callback = self._sub_map['matchOrders.*']
            callback(jdata)
        elif key.endswith('.liquidation_orders') and 'public.*.liquidation_orders' in self._sub_map:
            callback = self._sub_map['public.*.liquidation_orders']
            callback(jdata)
        elif key.endswith('.funding_rate') and 'public.*.funding_rate' in self._sub_map:
            callback = self._sub_map['public.*.funding_rate']
            callback(jdata)
        elif key.endswith('.contract_info') and 'public.*.contract_info' in self._sub_map:
            callback = self._sub_map['public.*.contract_info']
            callback(jdata)
        elif key.startswith('trigger_order_cross.') and 'trigger_order_cross.*' in self._sub_map:
            callback = self._sub_map['trigger_order_cross.*']
            callback(jdata)
        elif key.startswith('trigger_order.') and 'trigger_order.*' in self._sub_map:
            callback = self._sub_map['trigger_order.*']
            callback(jdata)
        elif key == 'accounts_cross':
            margin_account = jdata['data'][0]['margin_account'].lower()
            key = '{}.{}'.format(key, margin_account)
            if key in self._sub_map:
                callback = self._sub_map[key]
                callback(jdata)
            else:
                logger.error('no callbck for {}'.format(plain))
        elif key == 'accounts'  or key == 'positions_cross' or key == 'positions':
            contract_code = jdata['data'][0]['contract_code'].lower()
            key = '{}.{}'.format(key, contract_code)
            if key in self._sub_map:
                callback = self._sub_map[key]
                callback(jdata)
            else:
                logger.error('no callbck for {}'.format(plain))
        else:
            logger.error('no callbck for {}'.format(plain))
            return

    def _on_msg(self, message):
        plain = gzip.decompress(message).decode()
        jdata = json.loads(plain)
        if 'ping' in jdata:
            sdata = plain.replace('ping', 'pong')
            self._ws.send(sdata)
        elif 'op' in jdata:
            opdata = jdata['op']
            if opdata == 'ping':
                sdata = plain.replace('ping', 'pong')
                self._ws.send(sdata)
            elif opdata == 'auth':
                if jdata['err-code'] == 0:
                    self._auth = True
                logger.info(plain)
            elif opdata == 'sub':
                error_code = jdata['err-code']
                if error_code == 0:
                    id = jdata['cid']
                    ch = jdata['topic'].lower()
                    self._sub_map[ch] = self._sub_map[id]
                    del self._sub_map[id]
                logger.info(plain)
            elif opdata == 'unsub':
                id = jdata['topic']
                if id in self._sub_map:
                    del self._sub_map[id]
                logger.info(plain)
            elif opdata == 'notify':  # account/system data
                self._handle_notify(opdata, jdata, plain)
            else:
                logger.error('unknow data:\n{}'.format(plain))
        elif 'subbed' in jdata:  # sub success response
            id = jdata['id']
            ch = jdata['subbed']
            self._sub_map[ch] = self._sub_map[id]
            del self._sub_map[id]
            logger.info(plain)
        elif 'ch' in jdata:  # sub market/index data
            key = jdata['ch']
            if key not in self._sub_map:
                logger.error('no callbck for {}'.format(plain))
                return
            callback = self._sub_map[key]
            callback(jdata)
        elif 'rep' in jdata:  # rep data
            key = jdata['id']
            if key not in self._req_map:
                logger.error('no callbck for {}'.format(plain))
                return
            callback = self._req_map[key]
            callback(jdata)
            del self._req_map[key]
        else:
            logger.error('unknow data:\n{}'.format(plain))

    def _on_close(self):
        logger.info("ws close.")

    def _on_error(self, error):
        logger.error(error)

    def sub(self, req: dict, id: str, callback):
        data = json.dumps(req)

        while not self._has_open:
            time.sleep(1)

        if id in self._sub_map:
            self._sub_map[id] = callback
            return
        else:
            self._sub_map[id] = callback
        self._ws.send(data)
        logger.info(data)

    def unsub(self, req: dict, id: str):
        data = json.dumps(req)

        while not self._has_open:
            time.sleep(1)
        self._ws.send(data)
        logger.info(data)

    def req(self, req: dict, id: str, callback):
        data = json.dumps(req)

        while not self._has_open:
            time.sleep(1)

        if id in self._req_map:
            self._req_map[id] = callback
            return
        else:
            self._req_map[id] = callback
        self._ws.send(data)
        logger.info(data)

    def close(self):
        self._ws.close()
