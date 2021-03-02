import sys
import unittest
from config import *
import time

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.ws_account import *
from alpha.platforms.huobi_usdt_swap.logger import *


class TestWsAccount(unittest.TestCase):
    def _callback_1(self, jdata):
        logger.info('_callback_1:{}'.format(jdata))

    def _callback_2(self, jdata):
        logger.info('_callback_2:{}'.format(jdata))

    def test_sub(self):
        ws1 = WsAccount(config['access_key'], config['secret_key'])
        data = {"op": "sub", "topic": "accounts.BTC-USDT"}  
        ws1.sub(data, self._callback_1)

        ws2 = WsAccount(config['access_key'], config['secret_key'])
        data = {"op": "sub", "topic": "accounts_cross.*"}  
        ws2.sub(data, self._callback_2)

        time.sleep(30)
        data = {"op": "unsub", "topic": "accounts.BTC-USDT"}  
        ws1.unsub(data)
        data = {"op": "unsub", "topic": "accounts_cross.*"}  
        ws2.unsub(data)
        logger.info('unsub')

        time.sleep(10)
        ws1.close()
        ws2.close()
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
