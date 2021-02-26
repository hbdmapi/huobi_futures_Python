import websocket
import threading

import gzip
import json
from alpha.platforms.huobi_usdt_swap.logger import *
import time


class WsUtils:
    def __init__(self, path: str, host: str = None):
        if host is None:
            host = "api.btcgateway.pro"
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
        self._sub_map = {}
        self._req_map = {}

    def __del__(self):
        self.close()

    def _on_open(self):
        logger.info('ws open.')
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
                logger.info(plain)
                if jdata['err-code'] == 0:
                    self._auth = True
            elif opdata == 'notify': # account/system data
                pass
        elif 'subbed' in jdata: # sub success response
            logger.info(plain)
        elif 'ch' in jdata: # sub market/index data
            key = jdata['ch']
            key = key.lower()
            if key not in self._sub_map:
                logger.error('no callbck for {}'.format(plain))
                return
            callback = self._sub_map[key]
            callback(jdata)
        elif 'rep' in jdata: # rep data
            key = jdata['rep']
            key = key.lower()
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

    def sub(self, req: dict, key:str, callback):
        data = json.dumps(req)
        key = key.lower()

        while not self._has_open:
            time.sleep(1)

        if key in self._sub_map:
            self._sub_map[key] = callback
            return
        else:
            self._sub_map[key] = callback
        self._ws.send(data)
        logger.info(data)

    def req(self, req: dict, key:str, callback):
        data = json.dumps(req)
        key = key.lower()

        while not self._has_open:
            time.sleep(1)

        if key in self._req_map:
            self._req_map[key] = callback
            return
        else:
            self._req_map[key] = callback
        self._ws.send(data)
        logger.info(data)

    def close(self):
        self._ws.close()