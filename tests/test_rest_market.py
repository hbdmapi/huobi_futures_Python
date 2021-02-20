import logging
from alpha.platforms.huobi_usdt_swap.rest_market import *
import sys
import unittest
from config import *

sys.path.append('..')

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.level = logging.DEBUG
logger.addHandler(stream_handler)


class TestRestMarket(unittest.TestCase):
    def test_get_contract_info(self):
        api = RestMarket()
        result = api.get_contract_info(
            {"contract_code": "btc-usdt", "support_margin_mode": "all"})
        logger.info(result)
        self.assertEqual('ok', result['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
