# -*— coding:utf-8 -*-

"""
Huobi Swap Market Demo.

Author: QiaoXiaofeng
Date:   2020/1/10
Email:  andyjoe318@gmail.com
"""


import sys


def initialize():
    from strategy.strategy import MyStrategy
    MyStrategy()


def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = None

    from alpha.quant import quant
    quant.initialize(config_file)
    initialize()
    quant.start()


if __name__ == '__main__':
    main()
