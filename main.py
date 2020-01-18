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
        #Clist=[EOS]
        for ct in Clist:
            print("processing for ctype of %s"%(ct))
            current_id = zero_start
            current_id += 24 * 3600 * 30
            currency_type = ct
            model = Model()
            while current_id < now :
                boll_list = GetBollList(currency_type, 30, current_id)
                price_list = GetPriceList(currency_type, Day, 30, current_id)
                ma_list = GetMAList(currency_type, Day, 30, current_id)
                if len(price_list) < 2 or len(boll_list) < 2 or price_list[0].id_ != boll_list[0].id_:
                    log_warn("price list size %d, boll_list size %d in %d @ %s"%(len(price_list), len(boll_list), current_id, timestamp2dstring(current_id)))
                    current_id += 3600 * 24
                    continue
                if model.IsStatic(boll_list):
                    print("Buy: model static in %s@%d for %s"%(timestamp2dstring(current_id), current_id, currency_type))
                #boll曲线下轨道，在极小值, 当日收盘价在中轨至上,预示着下跌即将开始
                if model.IsBollLowest(boll_list) and boll_list[1].boll_low_ * 1.3 < boll_list[1].boll_high_ and price_list[1].close_ > boll_list[1].boll_mid_:
                    print("Sell: model bollLowest in %s@%d for %s"%(timestamp2dstring(current_id), current_id, currency_type))
                current_id += 3600 * 24
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description='run regression test cases by cases or groups'
    parser.add_argument("-g","--get", action="store", help="get data from web", dest="get", nargs="?", type=str)
    parser.add_argument("-f","--forecast", action="store", help="forecasting of offline", dest="forecast", nargs="?", type=str)
    args = parser.parse_args()

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
