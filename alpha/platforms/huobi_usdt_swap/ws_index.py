from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsIndex:
    def __init__(self, path: str, host: str = None):
        self.ws = WsUtils(path, host)

    def __del__(self):
        self.ws.close()

    def close(self):
        self.ws.close()

    def sub_index(self, contract_code: str, period: str, callback):
        ch = "market.{}.index.{}".format(contract_code, period)
        id = "sub_index_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_index(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.index.{}".format(contract_code, period)
        id = "req_index_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)

    def sub_premium_index(self, contract_code: str, period: str, callback):
        ch = "market.{}.premium_index.{}".format(contract_code, period)
        id = "sub_premium_index_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_premium_index(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.premium_index.{}".format(contract_code, period)
        id = "req_premium_index_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)

    def sub_estimated_rate(self, contract_code: str, period: str, callback):
        ch = "market.{}.estimated_rate.{}".format(contract_code, period)
        id = "sub_estimated_rate_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_estimated_rate(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.estimated_rate.{}".format(contract_code, period)
        id = "req_estimated_rate_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)


    def sub_basis(self, contract_code: str, period: str, callback):
        ch = "market.{}.basis.{}.open".format(contract_code, period)
        id = "sub_basis_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_basis(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.basis.{}.open".format(contract_code, period)
        id = "req_basis_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)


    def sub_mark_price(self, contract_code: str, period: str, callback):
        ch = "market.{}.mark_price.{}".format(contract_code, period)
        id = "sub_mark_price_{}_{}".format(contract_code, period)

        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, callback)

    def req_mark_price(self, contract_code: str, period: str, start: int, to: int, callback):
        ch = "market.{}.mark_price.{}".format(contract_code, period)
        id = "req_mark_price_{}_{}_{}_{}".format(contract_code, period, start, to)

        req = {"req": ch, "from": start, "to": to, "id": id}
        self.ws.req(req, id, callback)