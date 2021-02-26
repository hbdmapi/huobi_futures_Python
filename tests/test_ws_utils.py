import sys
import unittest
from config import *
import time

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.logger import *
from alpha.platforms.huobi_usdt_swap.ws_utils import *


class TestWsUtils(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.ws = WsUtils("/linear-swap-ws")

    def _callback_1(self, jdata):
        logger.info('_callback_1:{}'.format(jdata))

    def _callback_2(self, jdata):
        logger.info('_callback_2:{}'.format(jdata))

    def test_sub(self):
        ch = "market.BTC-USDT.kline.1min"
        req = {"sub": ch}
        self.ws.sub(req, ch, self._callback_1)

        ch = "market.ETH-USDT.kline.1min"
        req = {"sub": ch}
        self.ws.sub(req, ch, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req(self):
        ch = "market.BTC-USDT.kline.1min"
        req = {"req": ch, "from":1614320780, "to":1614321780}
        self.ws.req(req, ch, self._callback_1)

        ch = "market.ETH-USDT.kline.1min"
        req = {"req": ch, "from":1614320780, "to":1614321780}
        self.ws.req(req, ch, self._callback_2)

        self.ws.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
