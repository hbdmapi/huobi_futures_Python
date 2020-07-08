# -*- coding:utf-8 -*-

"""
some constants and global queues

Author: QiaoXiaofeng
Date:   2020/01/11
Email:  andyjoe318@gmail.com
"""

from collections import deque

# Version
VERSION = "1.0.10_200708_alpha"

# Exchange Names
HUOBI_SWAP = "huobi_swap"  # Huobi Swap https://huobiapi.github.io/docs/coin_margined_swap/v1/cn/
HUOBI_FUTURE = "huobi_future"  # Huobi Future https://huobiapi.github.io/docs/dm/v1/cn/#5ea2e0cde2
HUOBI_OPTION = "huobi_option" # Huobi Option 

# Market Types
MARKET_TYPE_TRADE = "trade"
MARKET_TYPE_ORDERBOOK = "orderbook"
MARKET_TYPE_KLINE = "kline"

# REQUEST AGENT 
USER_AGENT = "AlphaQuant" + VERSION
