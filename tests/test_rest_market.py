import sys
import unittest
from config import *

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.rest_market import *


class TestRestMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = RestMarket()

    def test_get_contract_info(self):
        result = self.api.get_contract_info(
            {"contract_code": "btc-usdt", "support_margin_mode": "all"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_index_info(self):
        result = self.api.get_index_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_price_limit(self):
        result = self.api.get_price_limit(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_open_interest(self):
        result = self.api.get_open_interest(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_depth(self):
        result = self.api.get_depth(
            {"contract_code": "btc-usdt", "type": "step0"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_bbo(self):
        result = self.api.get_bbo(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_kline(self):
        result = self.api.get_kline(
            {"contract_code": "btc-usdt", "period": "1min", "size": 10})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_mark_price_kline(self):
        result = self.api.get_mark_price_kline(
            {"contract_code": "btc-usdt", "period": "1min", "size": 10})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_merged(self):
        result = self.api.get_merged(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_batch_merged(self):
        result = self.api.get_batch_merged(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_trade(self):
        result = self.api.get_trade(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_history_trade(self):
        result = self.api.get_history_trade(
            {"contract_code": "btc-usdt", "size": 2000})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_risk_info(self):
        result = self.api.get_risk_info(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_insurance_fund(self):
        result = self.api.get_insurance_fund(
            {"contract_code": "btc-usdt", "page_index": 2, "page_size": 100})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_adjustfactor(self):
        result = self.api.isolated_get_adjustfactor(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_adjustfactor(self):
        result = self.api.cross_get_adjustfactor(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_estimated_settlement_price(self):
        result = self.api.get_estimated_settlement_price(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_open_interest(self):
        result = self.api.get_open_interest(
            {"contract_code": "btc-usdt", "period": "60min", "size": 100, "amount_type": 1})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_ladder_margin(self):
        result = self.api.isolated_get_ladder_margin(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_ladder_margin(self):
        result = self.api.cross_get_ladder_margin(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_elite_account_ratio(self):
        result = self.api.get_elite_account_ratio(
            {"contract_code": "btc-usdt", "period": "5min"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_elite_position_ratio(self):
        result = self.api.get_elite_position_ratio(
            {"contract_code": "btc-usdt", "period": "5min"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_api_state(self):
        result = self.api.isolated_get_api_state(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_transfer_state(self):
        result = self.api.cross_get_transfer_state(
            {"margin_account": "usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_trade_state(self):
        result = self.api.cross_get_trade_state(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_funding_rate(self):
        result = self.api.get_funding_rate(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_batch_funding_rate(self):
        result = self.api.get_batch_funding_rate()
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_historical_funding_rate(self):
        result = self.api.get_historical_funding_rate(
            {"contract_code": "btc-usdt", "page_index": 2, "page_size": 50})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_liquidation_orders(self):
        result = self.api.get_liquidation_orders(
            {"contract_code": "btc-usdt", "trade_type": 0, "create_date": 90, "page_index": 2, "page_size": 50})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_settlement_records(self):
        result = self.api.get_settlement_records(
            {"contract_code": "btc-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_premium_index_kline(self):
        result = self.api.get_premium_index_kline(
            {"contract_code": "btc-usdt", "period": "1min", "size": 100})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_estimated_rate_kline(self):
        result = self.api.get_estimated_rate_kline(
            {"contract_code": "btc-usdt", "period": "1min", "size": 100})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_get_basis(self):
        result = self.api.get_basis(
            {"contract_code": "btc-usdt", "period": "1min", "basis_price_type": "close", "size": 100})
        logger.info(result)
        self.assertEqual('ok', result['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
