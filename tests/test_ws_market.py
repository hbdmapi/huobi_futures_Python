import sys
import unittest
from config import *
import time

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.ws_market import *


class TestWsMarket(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.ws = WsMarket("/linear-swap-ws")

    def _callback_1(self, jdata):
        logger.info('_callback_1:{}'.format(jdata))

    def _callback_2(self, jdata):
        logger.info('_callback_2:{}'.format(jdata))

    def test_sub_kline(self):
        self.ws.sub_kline("btc-usdt", "1min", self._callback_1)
        self.ws.sub_kline("eth-usdt", "1min", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_kline(self):
        self.ws.req_kline("btc-usdt", "1min", 1614320780, 1614321780, self._callback_1)
        self.ws.req_kline("btc-usdt", "1min", 1614321780, 1614321780, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_depth(self):
        self.ws.sub_depth("btc-usdt", "step6", self._callback_1)
        self.ws.sub_depth("eth-usdt", "step6", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_depth_incremental(self):
        self.ws.sub_depth_incremental("btc-usdt", "size_20", self._callback_1)
        self.ws.sub_depth_incremental("eth-usdt", "size_20", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_detail(self):
        self.ws.sub_detail("btc-usdt", self._callback_1)
        self.ws.sub_detail("eth-usdt", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_bbo(self):
        self.ws.sub_bbo("btc-usdt", self._callback_1)
        self.ws.sub_bbo("eth-usdt", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_sub_trade_detail(self):
        self.ws.sub_trade_detail("btc-usdt", self._callback_1)
        self.ws.sub_trade_detail("eth-usdt", self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req_trade_detail(self):
        self.ws.req_trade_detail("btc-usdt", self._callback_1)
        self.ws.req_trade_detail("eth-usdt", self._callback_2)

        time.sleep(10)
        self.ws.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
