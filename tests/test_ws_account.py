import sys
import unittest
from config import *
import time

sys.path.append('..')
from alpha.platforms.huobi_usdt_swap.ws_account import *
from alpha.platforms.huobi_usdt_swap.logger import *


class TestWsAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ws = WsAccount("/linear-swap-notification",
                           config["access_key"], config["secret_key"])

    def _callback_1(self, jdata):
        logger.info('_callback_1:{}'.format(jdata))

    def _callback_2(self, jdata):
        logger.info('_callback_2:{}'.format(jdata))

    # orders
    def test_isolated_orders(self):
        self.ws.isolated_sub_orders("xrp-usdt", self._callback_1)
        self.ws.isolated_sub_orders("eth-usdt", self._callback_2)

        time.sleep(60)
        self.ws.isolated_unsub_orders("xrp-usdt")
        self.ws.isolated_unsub_orders("eth-usdt")

        logger.info('unsub')
        time.sleep(10)
        self.ws.close()

    def test_cross_orders(self):
        self.ws.cross_sub_orders("*", self._callback_1)

        time.sleep(60)
        self.ws.cross_unsub_orders("*")
        logger.info('unsub')
        time.sleep(10)
        self.ws.close()

    # accounts
    def test_isolated_accounts(self):
        self.ws.isolated_sub_accounts("xrp-usdt", self._callback_1)
        self.ws.isolated_sub_accounts("eth-usdt", self._callback_2)

        time.sleep(60)
        self.ws.isolated_unsub_accounts("xrp-usdt")
        self.ws.isolated_unsub_accounts("eth-usdt")

        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    def test_cross_accounts(self):
        self.ws.cross_sub_accounts("*", self._callback_1)

        time.sleep(30)
        self.ws.cross_unsub_accounts("*")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    # positions
    def test_isolated_positions(self):
        self.ws.isolated_sub_positions("xrp-usdt", self._callback_1)
        self.ws.isolated_sub_positions("eth-usdt", self._callback_2)

        time.sleep(30)
        self.ws.isolated_unsub_positions("xrp-usdt")
        self.ws.isolated_unsub_positions("eth-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    def test_cross_positions(self):
        self.ws.cross_sub_positions("xrp-usdt", self._callback_1)
        self.ws.cross_sub_positions("eth-usdt", self._callback_2)

        time.sleep(30)
        self.ws.cross_unsub_positions("xrp-usdt")
        self.ws.cross_unsub_positions("eth-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    # matchOrders
    def test_isolated_matchOrders(self):
        self.ws.isolated_sub_matchOrders("xrp-usdt", self._callback_1)
        self.ws.isolated_sub_matchOrders("eth-usdt", self._callback_2)

        time.sleep(30)
        self.ws.isolated_unsub_matchOrders("xrp-usdt")
        self.ws.isolated_unsub_matchOrders("eth-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    def test_cross_matchOrders(self):
        self.ws.cross_sub_matchOrders("xrp-usdt", self._callback_1)
        self.ws.cross_sub_matchOrders("eth-usdt", self._callback_2)

        time.sleep(30)
        self.ws.cross_unsub_matchOrders("xrp-usdt")
        self.ws.cross_unsub_matchOrders("eth-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    # liquidation_orders
    def test_liquidation_orders(self):
        self.ws.sub_liquidation_orders("xrp-usdt", self._callback_1)

        time.sleep(30)
        self.ws.unsub_liquidation_orders("xrp-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    # funding_rate
    def test_funding_rate(self):
        self.ws.sub_funding_rate("xrp-usdt", self._callback_1)

        time.sleep(30)
        self.ws.unsub_funding_rate("xrp-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    # contract_info
    def test_contract_info(self):
        self.ws.sub_contract_info("xrp-usdt", self._callback_1)

        time.sleep(30)
        self.ws.unsub_contract_info("xrp-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()
    
    # trigger_order
    def test_isolated_trigger_order(self):
        self.ws.isolated_sub_trigger_order("xrp-usdt", self._callback_1)
        self.ws.isolated_sub_trigger_order("eth-usdt", self._callback_2)

        time.sleep(30)
        self.ws.isolated_unsub_trigger_order("xrp-usdt")
        self.ws.isolated_unsub_trigger_order("eth-usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()

    def test_cross_trigger_order(self):
        self.ws.cross_sub_trigger_order("usdt", self._callback_1)

        time.sleep(30)
        self.ws.cross_unsub_trigger_order("usdt")
        logger.info('unsub')
        time.sleep(30)
        self.ws.close()



if __name__ == '__main__':
    unittest.main(verbosity=2)
