from alpha.platforms.huobi_usdt_swap.http_utils import *


class RestTriggerOrder:
    def __init__(self, access_key: str, secret_key: str, host: str = None):
        self.access_key = access_key
        self.secret_key = secret_key
        if host is None:
            host = "api.btcgateway.pro"
        self.host = host
    
    def isolated_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_trigger_order"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trigger_order"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_cancel(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_trigger_cancel"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_cancel(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trigger_cancel"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_cancel_all(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_trigger_cancelall"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_cancel_all(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trigger_cancelall"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_open_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_trigger_openorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_open_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trigger_openorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_his_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_trigger_hisorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_his_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trigger_hisorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_tpsl_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_tpsl_order"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_tpsl_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_tpsl_order"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_tpsl_cancel(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_tpsl_cancel"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_tpsl_cancel(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_tpsl_cancel"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_tpsl_cancel_all(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_tpsl_cancelall"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_tpsl_cancel_all(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_tpsl_cancelall"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_tpsl_open_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_tpsl_openorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_tpsl_open_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_tpsl_openorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_tpsl_his_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_tpsl_hisorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_tpsl_his_orders(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_tpsl_hisorders"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_relation_tpsl_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_relation_tpsl_order"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_relation_tpsl_order(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_relation_tpsl_order"
        return post(self.access_key, self.secret_key, self.host, path, data)