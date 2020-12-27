#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from forecast_model import *
from ds import *
from store import *
from hbapi import HuobiServices as api
import threading
import time
import argparse

#2017年11月1号为计算的起始点
zero_start = 1509465600
OneDay = 24 * 3600

def store():
    #Clist = [BTC]
    #Dlist = [Day]
    #Slist = [5, 10]
    for ct in Clist:
        for duration in Dlist:
            UpdatePrice(ct, duration, True)
            for step in Slist:
                UpdateMa(ct, duration, step, True)
        UpdateBoll(ct)

class Ticker(threading.Thread):
    def __init__(self, threadId, name) :
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.status = -1
        pass

    def run(self) :
        self.status = 0
        now  = int(time.time())
        log_info("Huang")
        Clist=[BTC]
        start_list = [0, 60, 120, 180, 240, 300, 360, 420]
        start_list = [180]
        for start_point in start_list:
            start_point = zero_start + start_point * OneDay
            for ct in Clist:
                log_info("processing for ctype of %s"%(ct))
                current_id = start_point
                currency_type = ct
                model = Model()
                asset = assets[currency_type]
                asset.Reset(10000.0)
                printStart = False
                while current_id < now :
                    current_id += 3600 * 24
                    boll_list = GetBollList(currency_type, 30, current_id)
                    price_list = GetPriceList(currency_type, Day, 30, current_id)
                    ma_list = GetMAList(currency_type, Day, 30, current_id)
                    if ma_list == None or price_list == None or boll_list == None:
                        log_warn("None data for %s @%s@"%(currency_type, timestamp2dstring(current_id)))
                        continue
                    if len(ma_list) != len(price_list) or len(ma_list) != len(boll_list) or len(ma_list) == 0:
                        log_warn("Zero/unEqual data for %s @%s@"%(currency_type, timestamp2dstring(current_id)))
                        continue
                    if ma_list[0].id_ != price_list[0].id_ or ma_list[0].id_ != boll_list[0].id_:
                        log_warn("Missed start data for %s @%s@"%(currency_type, timestamp2dstring(current_id)))
                        continue
                    if ma_list[-1].id_ != price_list[-1].id_ or ma_list[-1].id_ != boll_list[-1].id_:
                        log_warn("Missed end data for %s @%s@"%(currency_type, timestamp2dstring(current_id)))
                        continue

                    data_len = len(ma_list)
                    for index in range(len(ma_list)):
                        if ma_list[index].merge_mpb(price_list[index], boll_list[index]) == False:
                            data_len = index
                            break
                    if data_len < 15:
                        log_warn("No enough data for %s @%s@"%(currency_type, timestamp2dstring(current_id)))
                    data_list = ma_list[0:data_len]
                    today_data = data_list[0]
                    if printStart == False:
                        asset.Output(today_data.close_, "%-16s @%s@ : price %.2f"%("Simulate Start", timestamp2dstring(current_id), today_data.close_))
                        printStart = True

                    #Filter for sell
                    shouldNotSell = False
                    if len(asset.sell_list_) > 0:
                        #避免短期连续卖出
                        if (current_id - asset.sell_list_[-1].created_tid_ < 7 * OneDay):
                            shouldNotSell = True

                    #计算卖出参数
                    sell = TradeParam()
                    if shouldNotSell == True:
                        pass
                    else:
                        if today_data.CallBackFactor() >= 0.15 and sell.level < 30:
                            #巨大回调卖出
                            sell.factor = 0.5
                            sell.price = today_data.high_ * 0.85
                            sell.model = "cb"
                            sell.level = 30
                        vol_factor = today_data.CalculateMaSellVolFactor()
                        if vol_factor > 0 and sell.level < 20:
                            #均线卖出
                            sell.factor = vol_factor
                            sell.price = today_data.close_
                            sell.model = "ma"
                            sell.level = 20
                        if sell.level < 50 and model.RapidUpFactor(data_list) > 0 and model.Stable(data_list[3:17]) == False and today_data.ma60_ > today_data.open_:
                            #快速上涨卖出
                            sell.factor = 1.0
                            sell.price = min(today_data.open_ * 1.1, today_data.high_)
                            sell.model = "rp"
                            sell.level = 50

                    if sell.factor > 0:
                        asset.Sell(asset.ct_volume_ * sell.factor, sell.price, 0, current_id, sell.model)

                    #Fileter for buy
                    shouldNotBuy = False
                    if sell.factor > 0:
                        shouldNotBuy = True

                    if model.BollStableFactor(data_list[1:15], 0.20) < 0.8:
                        #稳定才买入
                        shouldNotBuy = True
                    if len(asset.buy_list_) > 0:
                        #避免短期连续买入
                        if (current_id - asset.buy_list_[-1].created_tid_ < 7 * OneDay):
                            shouldNotBuy = True

                    ##calculate buy factor
                    buy_factor = 0
                    buy_price = 0
                    buy_model = ""
                    if shouldNotBuy == True:
                        pass
                    elif model.BollStableFactor(data_list[0:21], 0.2) >= 0.8:
                        #定投策略
                        buy_factor = 0.2
                        buy_price = today_data.close_
                        buy_model = "sb"
                    else:
                        #均线买入策略
                        vol_factor = today_data.CalculateMaBuyVolFactor()
                        if vol_factor > 0:
                            buy_factor = vol_factor
                            buy_price = today_data.close_
                            buy_model = "ma"

                    if buy_factor > 0:
                        asset.Buy(0, buy_price, asset.Total(buy_price) * buy_factor, current_id, buy_model)
                        buy = True

                    #if model.IsBollLowest(boll_list) and boll_list[1].boll_low_ * 1.3 < boll_list[1].boll_high_ and price_list[1].close_ > boll_list[1].boll_mid_:
                    #    print("Sell: model bollLowest in %s@%d for %s"%(timestamp2dstring(current_id), current_id, currency_type))
                asset.Output(today_data.close_, "%-16s @%s@ : price %.2f"%("Simulate End", timestamp2dstring(current_id), today_data.close_))
        pass

class Store (threading.Thread):
    def __init__(self, threadId, name) :
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.status = -1
        pass

    def run(self) :
        self.status = 0
        while True:
            store()
            log_info("sleeping 1H for next round of store")
            time.sleep(600*2)
        pass

assets = {}
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description='run regression test cases by cases or groups'
    parser.add_argument("-g","--get", action="store", help="get data from web", dest="get", nargs="?", type=str)
    parser.add_argument("-f","--forecast", action="store", help="forecasting of offline", dest="forecast", nargs="?", type=str)
    args = parser.parse_args()

    for ct in Clist:
        asset = Asset(ct, 10000.0)
        assets[ct] = asset
    if args.get:
        storer = Store(1, "storer-1")
        storer.start()
        storer.join()
        log_info("main unexpected exit")
    if args.forecast:
        ticker= Ticker(1, "ticker-1")
        ticker.start()
        ticker.join()
        log_info("ticker and storer stoped")
    pass
