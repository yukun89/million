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
    def __init__(self):
        self.id_ = 0
        pass

    def SetClock(clock):
        self.id_ = clock
        pass

    def GetModels():
        pass

    ##横盘整理:最近1/2/4周，boll曲线波动率<10%的天数在80%以上
    def IsStatic(self, price_list, change_ratio = 0.1, valid_data_ratio = 0.8):
        boll_change_ratio = 0.10
        valid_data_ratio = 0.8
        if len(price_list) < 28:
            return False
        durations = [7, 14, 28]
        for duration in durations:
            dayNum = duration
            validDayNum = 0
            for index in range(dayNum):
                thisDayPrice = price_list[index]
                if thisDayPrice.boll_high_ < thisDayPrice.boll_low_ * (1 + boll_change_ratio):
                    validDayNum += 1
            if validDayNum  < dayNum * valid_data_ratio:
                return False
        return True
    def IsBollLowest(self, price_list):
        return price_list[1].boll_low_ * 1.003 < price_list[0].boll_low_ and price_list[1].boll_low_ * 1.003 < price_list[2].boll_low_
        pass
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
