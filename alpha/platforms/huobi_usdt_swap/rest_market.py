from alpha.platforms.huobi_usdt_swap.http_utils import *

class RestMarket:
    def __init__(self, host=None):
        if host is None:
            host = "api.btcgateway.pro"
        self.host = host

    def get_contract_info(self, params:dict=None)->json:
        path = "/linear-swap-api/v1/swap_contract_info"
        return get(self.host, path, params)
