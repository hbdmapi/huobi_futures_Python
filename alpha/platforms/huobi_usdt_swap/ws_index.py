from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsIndex(WsUtils):
    def __init__(self, host: str = None):
        super(WsIndex, self).__init__("/ws_index", host)

    def sub(self, data:dict, callback):
        self._sub(json.dumps(data), callback)

    def req(self, data:dict, callback):
        self._req(json.dumps(data), callback)