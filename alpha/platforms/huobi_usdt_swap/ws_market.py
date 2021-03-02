from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsMarket(WsUtils):
    def __init__(self, host: str = None):
        super(WsMarket, self).__init__("/linear-swap-ws", host)

    def sub(self, data:dict, callback):
        self._sub(json.dumps(data), callback)

    def req(self, data:dict, callback):
        self._req(json.dumps(data), callback)
