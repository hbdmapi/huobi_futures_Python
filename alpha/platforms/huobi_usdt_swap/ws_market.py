from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsMarket:
    def __init__(self, path: str, host: str = None):
        self.ws = WsUtils(path, host)

    def __del__(self):
        self.ws.close()

    def close(self):
        self.ws.close()

    def sub_kline(self, contract_code: str, period: str, callback):
        ch = "market.{}.kline.{}".format(contract_code, period)
        id = "sub_kline_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_kline(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.kline.{}".format(contract_code, period)
        id = "req_kline_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)

    def sub_depth(self, contract_code: str, stype: str, callback):
        ch = "market.{}.depth.{}".format(contract_code, stype)
        id = "sub_depth_{}_{}".format(contract_code, stype)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def sub_depth_incremental(self, contract_code: str, stype: str, callback):
        ch = "market.{}.depth.{}.high_freq".format(contract_code, stype)
        id = "sub_depth_incremental_{}_{}".format(contract_code, stype)

        req = {"sub": ch, "data_type": "incremental", "id": id}
        self.ws.sub(req, id, callback)

    def sub_detail(self, contract_code: str, callback):
        ch = "market.{}.detail".format(contract_code)
        id = "sub_detail_{}".format(contract_code)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def sub_bbo(self, contract_code: str, callback):
        ch = "market.{}.bbo".format(contract_code)
        id = "sub_bbo_{}".format(contract_code)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def sub_trade_detail(self, contract_code: str, callback):
        ch = "market.{}.trade.detail".format(contract_code)
        id = "sub_trade_detail_{}".format(contract_code)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_trade_detail(self, contract_code: str, callback, size: int = 50):
        ch = "market.{}.trade.detail".format(contract_code)
        id = "req_trade_detail_{}_{}_{}".format(contract_code, size, int(time.time()))

        req = {"req": ch, "size": size, "id": id}
        self.ws.req(req, id, callback)
