import sys
import unittest
from config import *

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.rest_transfer import *


class TestRestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = RestTransfer(config["access_key"], config["secret_key"])

    def test_transfer(self):
        result = self.api.transfer(
            {"from": "linear-swap", "to": "spot", "currency": "usdt", "amount": 1, "margin-account": "usdt"})
        logger.info(result)
        self.assertEqual(True, result['success'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
