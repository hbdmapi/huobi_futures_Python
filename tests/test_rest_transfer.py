import logging
from alpha.platforms.huobi_usdt_swap.rest_transfer import *
import sys
import unittest
from config import *

sys.path.append('..')

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.level = logging.DEBUG
logger.addHandler(stream_handler)


class TestRestAccount(unittest.TestCase):

    def setUp(self):
        self.api = RestTransfer(config["access_key"], config["secret_key"])

    def test_transfer(self):
        result = self.api.transfer(
            {"from": "linear-swap", "to": "spot", "currency": "usdt", "amount": 1, "margin-account": "usdt"})
        logger.info(result)
        self.assertEqual(True, result['success'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
