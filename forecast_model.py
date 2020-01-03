#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ds import *
from store import *
from hbapi import HuobiServices as api

#中期模型预测，有以下几种行情
#1.盘整行情
#2.上涨开启
#3.上涨持续行情
#4.上涨终止，即将下跌行情
#5.持续下跌行情
#6.超跌反弹行情

#一般行情的变化规律为1-2-3-4-5-6-5-6....1.
class Model:

    #引入一个指标：boll曲线波动率(High - Low)/Mid
    def __init__(self, currency_type):
        self.currency_type_ = currency_type
        self.id_ = 0
        pass

    def SetClock(clock):
        self.id_ = clock
        pass

    def GetModels():
        pass

    ##横盘整理:最近1/2/4周，boll曲线波动率<5%
    def IsStatic(boll_list):
        boll_change_ratio = map
        pass

    ##5% < delta_boll_ratio_30 < 10% && delta_boll_ratio_30 < delta_boll_ratio_14 < delta_boll_ratio_7 && M5 > M10 > M20
    def IsUpStart():
        pass

    def IsUpGoing():
        pass

    #delta_boll_ratio_30 > 30%
    #delta_boll_ratio_14 > 40%
    #delta_boll_ratio_7 > 50%
    #High > boll_Mid * 20%
    #IsUpNeedle
    def IsUpEnding():
        pass

    def IsDownStart():
        return IsUpEnding()

    def IsDownGoing():
        pass

    def IsDownEnding():
        pass
