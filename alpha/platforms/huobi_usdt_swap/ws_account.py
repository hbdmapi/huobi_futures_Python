from alpha.platforms.huobi_usdt_swap.ws_utils import *


class WsAccount:
    def __init__(self, path: str, access_key: str, secret_key: str, host: str = None):
        self.ws = WsUtils(path, host, access_key, secret_key)

    def __del__(self):
        self.ws.close()

    def close(self):
        self.ws.close()

    # orders
    def isolated_sub_orders(self, contract_code: str, callback):
        ch = "orders.{}".format(contract_code)
        cid = "sub_orders_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def isolated_unsub_orders(self, contract_code: str):
        ch = "orders.{}".format(contract_code)
        cid = "sub_orders_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    def cross_sub_orders(self, contract_code: str, callback):
        ch = "orders_cross.{}".format(contract_code)
        cid = "sub_orders_cross_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def cross_unsub_orders(self, contract_code: str):
        ch = "orders_cross.{}".format(contract_code)
        cid = "sub_orders_cross_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # accounts
    def isolated_sub_accounts(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "accounts.{}".format(contract_code)
        cid = "sub_accounts_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def isolated_unsub_accounts(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "accounts.{}".format(contract_code)
        cid = "sub_accounts_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    def cross_sub_accounts(self, margin_account: str, callback):
        margin_account = margin_account.lower()
        ch = "accounts_cross.{}".format(margin_account)
        cid = "sub_accounts_cross_{}".format(margin_account)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def cross_unsub_accounts(self, margin_account: str):
        margin_account = margin_account.lower()
        ch = "accounts_cross.{}".format(margin_account)
        cid = "sub_accounts_cross_{}".format(margin_account)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # positions
    def isolated_sub_positions(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "positions.{}".format(contract_code)
        cid = "sub_positions_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def isolated_unsub_positions(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "positions.{}".format(contract_code)
        cid = "sub_positions_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    def cross_sub_positions(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "positions_cross.{}".format(contract_code)
        cid = "sub_positions_cross_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def cross_unsub_positions(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "positions_cross.{}".format(contract_code)
        cid = "sub_positions_cross_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # matchOrders
    def isolated_sub_matchOrders(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "matchOrders.{}".format(contract_code)
        cid = "sub_matchOrders_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def isolated_unsub_matchOrders(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "matchOrders.{}".format(contract_code)
        cid = "sub_matchOrders_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    def cross_sub_matchOrders(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "matchOrders_cross.{}".format(contract_code)
        cid = "sub_matchOrders_cross_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def cross_unsub_matchOrders(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "matchOrders_cross.{}".format(contract_code)
        cid = "sub_matchOrders_cross_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # liquidation_orders
    def sub_liquidation_orders(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "public.{}.liquidation_orders".format(contract_code)
        cid = "sub_liquidation_orders_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def unsub_liquidation_orders(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "public.{}.liquidation_orders".format(contract_code)
        cid = "sub_liquidation_orders_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # funding_rate
    def sub_funding_rate(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "public.{}.funding_rate".format(contract_code)
        cid = "sub_funding_rate_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def unsub_funding_rate(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "public.{}.funding_rate".format(contract_code)
        cid = "sub_funding_rate_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # contract_info
    def sub_contract_info(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "public.{}.contract_info".format(contract_code)
        cid = "sub_contract_info_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def unsub_contract_info(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "public.{}.contract_info".format(contract_code)
        cid = "sub_contract_info_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    # trigger_order
    def isolated_sub_trigger_order(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "trigger_order.{}".format(contract_code)
        cid = "sub_trigger_order_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def isolated_unsub_trigger_order(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "trigger_order.{}".format(contract_code)
        cid = "sub_trigger_order_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)

    def cross_sub_trigger_order(self, contract_code: str, callback):
        contract_code = contract_code.lower()
        ch = "trigger_order_cross.{}".format(contract_code)
        cid = "sub_trigger_order_cross_{}".format(contract_code)

        req = {"op": "sub", "topic": ch, "cid": cid}
        self.ws.sub(req, cid, callback)

    def cross_unsub_trigger_order(self, contract_code: str):
        contract_code = contract_code.lower()
        ch = "trigger_order_cross.{}".format(contract_code)
        cid = "sub_trigger_order_cross_{}".format(contract_code)

        req = {"op": "unsub", "topic": ch, "cid": cid}
        self.ws.unsub(req, cid)
