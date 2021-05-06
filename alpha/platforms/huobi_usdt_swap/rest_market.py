from alpha.platforms.huobi_usdt_swap.http_utils import *


class RestMarket:
    def __init__(self, host=None):
        if host is None:
            host = "api.btcgateway.pro"
        self.host = host

    def get_contract_info(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_contract_info"
        return get(self.host, path, params)

    def get_index_info(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_index"
        return get(self.host, path, params)

    def get_price_limit(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_price_limit"
        return get(self.host, path, params)

    def get_open_interest(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_open_interest"
        return get(self.host, path, params)

    def get_depth(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/depth"
        return get(self.host, path, params)

    def get_bbo(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/bbo"
        return get(self.host, path, params)

    def get_kline(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/history/kline"
        return get(self.host, path, params)

    def get_mark_price_kline(self, params: dict = None) -> json:
        path = "/index/market/history/linear_swap_mark_price_kline"
        return get(self.host, path, params)

    def get_merged(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/detail/merged"
        return get(self.host, path, params)

    def get_batch_merged(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/detail/batch_merged"
        return get(self.host, path, params)

    def get_trade(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/trade"
        return get(self.host, path, params)

    def get_history_trade(self, params: dict = None) -> json:
        path = "/linear-swap-ex/market/history/trade"
        return get(self.host, path, params)

    def get_risk_info(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_risk_info"
        return get(self.host, path, params)

    def get_insurance_fund(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_insurance_fund"
        return get(self.host, path, params)

    def isolated_get_adjustfactor(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_adjustfactor"
        return get(self.host, path, params)

    def cross_get_adjustfactor(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_adjustfactor"
        return get(self.host, path, params)
    
    def get_estimated_settlement_price(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_estimated_settlement_price"
        return get(self.host, path, params)

    def get_open_interest(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_his_open_interest"
        return get(self.host, path, params)

    def isolated_get_ladder_margin(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_ladder_margin"
        return get(self.host, path, params)

    def cross_get_ladder_margin(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_ladder_margin"
        return get(self.host, path, params)

    def get_elite_account_ratio(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_elite_account_ratio"
        return get(self.host, path, params)

    def get_elite_position_ratio(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_elite_position_ratio"
        return get(self.host, path, params)

    def isolated_get_api_state(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_api_state"
        return get(self.host, path, params)

    def cross_get_transfer_state(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_transfer_state"
        return get(self.host, path, params)

    def cross_get_trade_state(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_trade_state"
        return get(self.host, path, params)

    def get_funding_rate(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_funding_rate"
        return get(self.host, path, params)

    def get_batch_funding_rate(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_batch_funding_rate"
        return get(self.host, path, params)

    def get_historical_funding_rate(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_historical_funding_rate"
        return get(self.host, path, params)

    def get_liquidation_orders(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_liquidation_orders"
        return get(self.host, path, params)

    def get_settlement_records(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_settlement_records"
        return get(self.host, path, params)

    def get_premium_index_kline(self, params: dict = None) -> json:
        path = "/index/market/history/linear_swap_premium_index_kline"
        return get(self.host, path, params)

    def get_estimated_rate_kline(self, params: dict = None) -> json:
        path = "/index/market/history/linear_swap_estimated_rate_kline"
        return get(self.host, path, params)

    def get_basis(self, params: dict = None) -> json:
        path = "/index/market/history/linear_swap_basis"
        return get(self.host, path, params)