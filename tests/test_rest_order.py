import logging
from alpha.platforms.huobi_usdt_swap.rest_order import *
import sys
import unittest
from config import *

sys.path.append('..')

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.level = logging.DEBUG
logger.addHandler(stream_handler)


class TestRestOrder(unittest.TestCase):

    def setUp(self):
        self.api = RestOrder(config["access_key"], config["secret_key"])

    def test_isolated_order(self):
        result = self.api.isolated_order(
            {"contract_code": "eos-usdt", "price": 5, "volume": 1, "direction": "buy", "offset": "open", "lever_rate": 10, "order_price_type": "limit"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_order(self):
        result = self.api.cross_order(
            {"contract_code": "eos-usdt", "price": 5, "volume": 1, "direction": "buy", "offset": "open", "lever_rate": 10, "order_price_type": "limit"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_batch_order(self):
        result = self.api.isolated_batch_order(
            {"orders_data":[{"contract_code": "eos-usdt", "price": 5, "volume": 1, "direction": "buy", "offset": "open", "lever_rate": 10, "order_price_type": "limit"}]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_batch_order(self):
        result = self.api.cross_batch_order(
            {"orders_data":[{"contract_code": "eos-usdt", "price": 5, "volume": 1, "direction": "buy", "offset": "open", "lever_rate": 10, "order_price_type": "limit"}]})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_cancel(self):
        result = self.api.isolated_cancel(
            {"contract_code": "eos-usdt", "order_id": "813439565485744129"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_cancel(self):
        result = self.api.cross_cancel(
            {"contract_code": "eos-usdt", "order_id": "813439550126292992"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_cancel_all(self):
        result = self.api.isolated_cancel_all(
            {"contract_code": "eos-usdt", "direction": "buy", "offset": "open"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_cancel_all(self):
        result = self.api.cross_cancel_all(
            {"contract_code": "eos-usdt", "direction": "buy", "offset": "open"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_switch_lever_rate(self):
        result = self.api.isolated_switch_lever_rate(
            {"contract_code": "eos-usdt", "lever_rate": 20})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_switch_lever_rate(self):
        result = self.api.cross_switch_lever_rate(
            {"contract_code": "eos-usdt", "lever_rate": 20})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_order_info(self):
        result = self.api.isolated_get_order_info(
            {"contract_code": "eos-usdt", "order_id": "813439565485744129"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_order_info(self):
        result = self.api.cross_get_order_info(
            {"contract_code": "eos-usdt", "order_id": "813439550126292992"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_order_detail(self):
        result = self.api.isolated_get_order_detail(
            {"contract_code": "eos-usdt", "order_id": "813439565485744129"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_order_detail(self):
        result = self.api.cross_get_order_detail(
            {"contract_code": "eos-usdt", "order_id": "813439550126292992"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_open_orders(self):
        result = self.api.isolated_get_open_orders(
            {"contract_code": "eos-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_open_orders(self):
        result = self.api.cross_get_open_orders(
            {"contract_code": "eos-usdt"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_his_orders(self):
        result = self.api.isolated_get_his_orders(
            {"contract_code": "eos-usdt", "trade_type": 0, "type": 1, "status": "0", "create_date": 90})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_his_orders(self):
        result = self.api.cross_get_his_orders(
            {"contract_code": "eos-usdt", "trade_type": 0, "type": 1, "status": "0", "create_date": 90})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_his_orders_exact(self):
        result = self.api.isolated_get_his_orders_exact(
            {"contract_code": "eos-usdt", "trade_type": 0, "type": 1, "status": "0"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_his_orders_exact(self):
        result = self.api.cross_get_his_orders_exact(
            {"contract_code": "eos-usdt", "trade_type": 0, "type": 1, "status": "0"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_match_results(self):
        result = self.api.isolated_get_match_results(
            {"contract_code": "eos-usdt", "trade_type": 0, "create_date": 90})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_match_results(self):
        result = self.api.cross_get_match_results(
            {"contract_code": "eos-usdt", "trade_type": 0, "create_date": 90})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_get_match_results_exact(self):
        result = self.api.isolated_get_match_results_exact(
            {"contract_code": "eos-usdt", "trade_type": 0})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_get_match_results_exact(self):
        result = self.api.cross_get_match_results_exact(
            {"contract_code": "eos-usdt", "trade_type": 0})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_isolated_lightning_close_position(self):
        result = self.api.isolated_lightning_close_position(
            {"contract_code": "eos-usdt", "volume": 1, "direction": "sell"})
        logger.info(result)
        self.assertEqual('ok', result['status'])

    def test_cross_lightning_close_position(self):
        result = self.api.cross_lightning_close_position(
            {"contract_code": "eos-usdt", "volume": 1, "direction": "sell"})
        logger.info(result)
        self.assertEqual('ok', result['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
