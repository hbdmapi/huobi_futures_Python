import sys
import unittest
from config import *
import time

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.ws_index import *


class TestWsIndex(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.ws = WsIndex("/ws_index")

    def _callback_1(self, jdata):
        logger.info('_callback_1:{}'.format(jdata))

    def _callback_2(self, jdata):
        logger.info('_callback_2:{}'.format(jdata))

    def test_sub_index(self):
        self.ws.sub_index("btc-usdt", "1min", self._callback_1)
        self.ws.sub_index("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_index(self):
        self.ws.req_index("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_index("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_premium_index(self):
        self.ws.sub_premium_index("btc-usdt", "1min", self._callback_1)
        self.ws.sub_premium_index("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_premium_index(self):
        self.ws.req_premium_index("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_premium_index("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_estimated_rate(self):
        self.ws.sub_estimated_rate("btc-usdt", "1min", self._callback_1)
        self.ws.sub_estimated_rate("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_estimated_rate(self):
        self.ws.req_estimated_rate("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_estimated_rate("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_basis(self):
        self.ws.sub_basis("btc-usdt", "1min", self._callback_1)
        self.ws.sub_basis("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_basis(self):
        self.ws.req_basis("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_basis("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_mark_price(self):
        self.ws.sub_mark_price("btc-usdt", "1min", self._callback_1)
        self.ws.sub_mark_price("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_mark_price(self):
        self.ws.req_mark_price("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_mark_price("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
