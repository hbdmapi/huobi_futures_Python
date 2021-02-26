import sys
import unittest
from config import *

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.http_utils import *
from alpha.platforms.huobi_usdt_swap.logger import *


class TestHttpUtils(unittest.TestCase):
    def test_get(self):
        result = get(
            config['host'], '/linear-swap-api/v1/swap_contract_info', {'contract_code': 'BTC-USDT'})
        self.assertEqual('ok', result['status'])

    def test_post(self):
        result = post(config['access_key'], config['secret_key'], config['host'],
                      '/linear-swap-api/v1/swap_cross_account_info', {'margin_account': 'USDT'})
        self.assertEqual('ok', result['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
