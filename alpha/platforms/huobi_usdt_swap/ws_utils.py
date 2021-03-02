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

        self._sub_str = None
        self._sub_callback = None
        self._req_callback = None
        self._active_close = False

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
        logger.debug(data)

    def _on_open(self):
        logger.info('ws open.')
        if self._auth == False:
            self._send_auth_data('get', self._path, self._host,
                                 self._access_key, self._secret_key)
        self._has_open = True

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
                logger.info(plain)
            elif opdata == 'unsub':
                logger.info(plain)
            elif opdata == 'notify':
                if self._sub_callback is not None:
                    self._sub_callback(jdata)
            else:
                pass
        elif 'subbed' in jdata:
            logger.info(plain)
        elif 'ch' in jdata:
            if self._sub_callback is not None:
                self._sub_callback(jdata)
        elif 'rep' in jdata:
            if self._req_callback is not None:
                self._req_callback(jdata)
                self._req_callback = None
        else:
            pass

    def _on_close(self):
        logger.info("ws close.")
        if not self._active_close and self._sub_str is not None:
            self.sub(self._sub_str, self._sub_callback)

    def _on_error(self, error):
        logger.error(error)

    def _sub(self, sub_str: str, callback):
        while not self._has_open:
            time.sleep(1)

        self._sub_str = sub_str
        self._sub_callback = callback
        self._ws.send(sub_str)
        logger.debug(sub_str)

    def _unsub(self, unsub_str: str):
        while not self._has_open:
            time.sleep(1)
        
        self._sub_str = None
        self._sub_callback = None
        self._ws.send(unsub_str)
        logger.debug(unsub_str)

    def _req(self, req_str: str, callback):
        while not self._has_open:
            time.sleep(1)
            
        self._req_callback = callback
        self._ws.send(req_str)
        logger.info(req_str)

    def close(self):
        self._active_close = True
        self._sub_str = None
        self._sub_callback = None
        self._req_callback = None
        self._ws.close()
