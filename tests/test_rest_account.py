import sys
import unittest
from config import *

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.rest_account import *


class TestRestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = RestAccount(config["access_key"], config["secret_key"])

    def test_isolated_get_account_info(self):
        result = self.api.isolated_get_account_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_account_info(self):
        result = self.api.cross_get_account_info(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_position_info(self):
        result = self.api.isolated_get_position_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_position_info(self):
        result = self.api.cross_get_position_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_account_position_info(self):
        result = self.api.isolated_get_account_position_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_account_position_info(self):
        result = self.api.cross_get_account_position_info(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_set_sub_auth(self):
        result = self.api.set_sub_auth(
            {"sub_uid": config["sub_uid"], "sub_auth": 1})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_sub_account_list(self):
        result = self.api.isolated_get_sub_account_list(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_sub_account_list(self):
        result = self.api.cross_get_sub_account_list(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_sub_account_info_list(self):
        result = self.api.isolated_get_sub_account_info_list(
            {"contract_code": "btc-usdt", "page_index": 1, "page_size": 20})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_sub_account_info_list(self):
        result = self.api.cross_get_sub_account_info_list(
            {"margin_account": "usdt", "page_index": 1, "page_size": 20})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_sub_account_info(self):
        result = self.api.isolated_get_sub_account_info(
            {"contract_code": "btc-usdt", "sub_uid": config["sub_uid"]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_sub_account_info(self):
        result = self.api.cross_get_sub_account_info(
            {"margin_account": "usdt", "sub_uid": config["sub_uid"]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_sub_position_info(self):
        result = self.api.isolated_get_sub_position_info(
            {"contract_code": "btc-usdt", "sub_uid": config["sub_uid"]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_sub_position_info(self):
        result = self.api.cross_get_sub_position_info(
            {"contract_code": "btc-usdt", "sub_uid": config["sub_uid"]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_financial_record(self):
        result = self.api.get_financial_record(
            {"margin_account": "usdt", "contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_financial_record_exact(self):
        result = self.api.get_financial_record_exact(
            {"margin_account": "usdt", "contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_user_settlement_records(self):
        result = self.api.isolated_get_user_settlement_records(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_user_settlement_records(self):
        result = self.api.cross_get_user_settlement_records(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_available_level_rate(self):
        result = self.api.isolated_get_available_level_rate(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_available_level_rate(self):
        result = self.api.cross_get_available_level_rate(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_order_limit(self):
        result = self.api.get_order_limit(
            {"contract_code": "btc-usdt", "order_price_type": "limit"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_fee(self):
        result = self.api.get_fee(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_transfer_limit(self):
        result = self.api.isolated_get_transfer_limit(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_transfer_limit(self):
        result = self.api.cross_get_transfer_limit(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_position_limit(self):
        result = self.api.isolated_get_position_limit(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_position_limit(self):
        result = self.api.cross_get_position_limit(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_master_sub_transfer(self):
        result = self.api.master_sub_transfer(
            {"sub_uid": config["sub_uid"], "asset": "usdt", "from_margin_account": "USDT", "to_margin_account": "usdt", "amount": 1, "type": "master_to_sub"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_master_sub_transfer_record(self):
        result = self.api.get_master_sub_transfer_record(
            {"margin_account": "usdt", "create_date": 90})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_transfer_inner(self):
        result = self.api.transfer_inner(
            {"asset": "usdt", "from_margin_account": "USDT", "to_margin_account": "btc-usdt", "amount": 1})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_api_trading_status(self):
        result = self.api.get_api_trading_status()
        logger.info(result)
        self.assertEqual('ok', result['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
