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

    def GetModels():
        pass

    def Stable(self, price_list):
        factor = 0
        length = len(price_list)
        if length < 1:
            return
        array = price_list
        close_price_list = [x.close_ for x in array]
        avg  = sum(close_price_list)/length
        variance = sum([(avg - x)*(avg - x) for x in close_price_list])/length
        std_variance = variance ** 0.5

        diff_percent = 0
        max_value = 0
        min_value = 1000000
        for data in price_list:
            if data.high_ > 1.15 * data.low_:
                return False
            if data.high_ > max_value:
                max_value = data.high_
            if data.low_ < max_value:
                max_value = data.low_

        if max_value > 1.2 * min_value:
            return False

        return float(std_variance)/float(avg) < 0.01

    def BollStableFactor(self, price_list, boll_change_ratio = 0.15):
        boll_change_ratio = boll_change_ratio
        valid_data_ratio = 0.8
        dayNum = len(price_list)
        if dayNum == 0:
            return 0.0
        validDayNum = 0
        for index in range(dayNum):
            thisDayPrice = price_list[index]
            if thisDayPrice.boll_high_ < thisDayPrice.boll_low_ * (1 + boll_change_ratio):
                max_value = max(thisDayPrice.open_, thisDayPrice.close_)
                min_value = min(thisDayPrice.open_, thisDayPrice.close_)
                if max_value < 1.08 * min_value:
                    validDayNum += 1
        return 1.0 * validDayNum / dayNum

    def IsBollLowest(self, price_list):
        return price_list[1].boll_low_ * 1.003 < price_list[0].boll_low_ and price_list[1].boll_low_ * 1.003 < price_list[2].boll_low_
        pass


    def RapidUpFactor(self, datas):

        #极速上涨，应该卖出 15pp/1day, 25pp/2day, 30pp/3day
        rapid_factor = 0
        if datas[0].high_ > 1.15 * datas[0].open_:
            rapid_factor = 1
        elif datas[1].high_ > 1.25 * datas[0].open_:
            rapid_factor = 1
        elif datas[3].high_ > 1.30 * datas[0].open_:
            rapid_factor = 1

        return rapid_factor

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
