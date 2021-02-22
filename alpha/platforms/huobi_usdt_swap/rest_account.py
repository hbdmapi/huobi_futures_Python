from alpha.platforms.huobi_usdt_swap.http_utils import *


class RestAccount:
    def __init__(self, access_key: str, secret_key: str, host: str = None):
        self.access_key = access_key
        self.secret_key = secret_key
        if host is None:
            host = "api.btcgateway.pro"
        self.host = host
    
    def isolated_get_account_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_account_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_account_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_account_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_account_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_account_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_account_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_account_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def set_sub_auth(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_sub_auth"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_sub_account_list(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_sub_account_list"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_sub_account_list(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_sub_account_list"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_sub_account_info_list(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_sub_account_info_list"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_sub_account_info_list(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_sub_account_info_list"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_sub_account_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_sub_account_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_sub_account_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_sub_account_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_sub_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_sub_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_sub_position_info(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_sub_position_info"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_financial_record(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_financial_record"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_financial_record_exact(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_financial_record_exact"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_user_settlement_records(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_user_settlement_records"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_user_settlement_records(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_user_settlement_records"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_available_level_rate(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_available_level_rate"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_available_level_rate(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_available_level_rate"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_order_limit(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_order_limit"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_fee(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_fee"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_transfer_limit(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_transfer_limit"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_transfer_limit(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_transfer_limit"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def isolated_get_position_limit(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_position_limit"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def cross_get_position_limit(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_cross_position_limit"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def master_sub_transfer(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_master_sub_transfer"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_master_sub_transfer_record(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_master_sub_transfer_record"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def transfer_inner(self, data: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_transfer_inner"
        return post(self.access_key, self.secret_key, self.host, path, data)

    def get_api_trading_status(self, params: dict = None) -> json:
        path = "/linear-swap-api/v1/swap_api_trading_status"
        path = "{}?{}".format(path, get_url_suffix('get', self.access_key, self.secret_key, self.host, path))
        return get(self.host, path)
        