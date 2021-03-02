from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsAccount(WsUtils):
    def __init__(self, access_key: str, secret_key: str, host: str = None):
        super(WsAccount, self).__init__("/linear-swap-notification", host, access_key, secret_key)

    def sub(self, data:dict, callback):
        self._sub(json.dumps(data), callback)

    def unsub(self, data:dict):
        self._unsub(json.dumps(data))
        