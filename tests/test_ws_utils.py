from alpha.platforms.huobi_usdt_swap.ws_utils import *
from alpha.platforms.huobi_usdt_swap.logger import *
import sys
import unittest
from config import *
import time

sys.path.append('..')


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
        id = "btc-usdt"
        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, self._callback_1)

        ch = "market.ETH-USDT.kline.1min"
        id = "eth-usdt"
        req = {"sub": ch, "id": id}
        self.ws.sub(req, id, self._callback_2)

        time.sleep(10)
        self.ws.close()

    def test_req(self):
        ch = "market.BTC-USDT.kline.1min"
        id = "btc-usdt"
        req = {"req": ch, "from": 1614320780, "to": 1614321780, "id": id}
        self.ws.req(req, id, self._callback_1)

        ch = "market.ETH-USDT.kline.1min"
        id = "eth-usdt"
        req = {"req": ch, "from": 1614320780, "to": 1614321780, "id": id}
        self.ws.req(req, id, self._callback_2)

        time.sleep(10)
        self.ws.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
