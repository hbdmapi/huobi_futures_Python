# -*- coding:utf-8 -*-

"""
持仓对象

Author: Qiaoxiaofeng
Date:   2019/11/04
"""

from alpha.utils import tools


class Position:
    """ 持仓对象
    """

    def __init__(self, platform=None, account=None, strategy=None, symbol=None, leverage=None,\
        short_quantity=None, short_avg_price=None, short_pnl_ratio=None, short_pnl_unreal=None,\
           short_pnl=None, long_quantity=None, long_avg_price=None,  long_pnl_ratio=None, long_pnl_unreal=None,\
             long_pnl=None, long_pos_margin=None,  short_pos_margin=None, liquid_price=None, maint_margin_ratio=None, utime=None ):
        """ 初始化持仓对象
        @param platform 交易平台
        @param account 账户
        @param strategy 策略名称
        @param symbol 合约名称
        """
        self.platform = platform
        self.account = account
        self.strategy = strategy
        self.symbol = symbol
        self.leverage = leverage # 杠杆倍数
        self.short_quantity = short_quantity  # 空仓数量
        self.short_avg_price = short_avg_price  # 空仓持仓平均价格
        self.short_pnl_ratio = short_pnl_ratio # 空仓收益率
        self.short_pnl_unreal = short_pnl_unreal # 空仓未实现盈亏
        self.short_pnl = short_pnl # 空仓已实现盈亏
        self.long_quantity = long_quantity  # 多仓数量
        self.long_avg_price = long_avg_price  # 多仓持仓平均价格
        self.long_pnl_ratio = long_pnl_ratio # 多仓收益率
        self.long_pnl_unreal = long_pnl_unreal # 多仓未实现盈亏
        self.long_pnl = long_pnl # 多仓已实现盈亏
        self.long_pos_margin = long_pos_margin # 多仓持仓保证金 
        self.short_pos_margin = short_pos_margin #  空仓持仓保证金 
        self.liquid_price = liquid_price  # 预估爆仓价格
        self.maint_margin_ratio = maint_margin_ratio #  保证金率
        self.utime = utime if utime else tools.get_cur_timestamp_ms()

    def update(self, short_quantity=0, short_avg_price=0, long_quantity=0, long_avg_price=0, liquid_price=0,
               utime=None):
        self.short_quantity = short_quantity
        self.short_avg_price = short_avg_price
        self.long_quantity = long_quantity
        self.long_avg_price = long_avg_price
        self.liquid_price = liquid_price
        self.utime = utime if utime else tools.get_cur_timestamp_ms()

    def __str__(self):
        info = "[platform: {platform}, account: {account}, strategy: {strategy}, symbol: {symbol}, " \
               "short_quantity: {short_quantity}, short_avg_price: {short_avg_price}, " \
               "long_quantity: {long_quantity}, long_avg_price: {long_avg_price}, liquid_price: {liquid_price}, " \
               "utime: {utime}]"\
            .format(platform=self.platform, account=self.account, strategy=self.strategy, symbol=self.symbol,
                    short_quantity=self.short_quantity, short_avg_price=self.short_avg_price,
                    long_quantity=self.long_quantity, long_avg_price=self.long_avg_price,
                    liquid_price=self.liquid_price, utime=self.utime)
        return info

    def __repr__(self):
        return str(self)