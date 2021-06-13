#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : main.py
# Date              : 29.12.2020
# Last Modified Date: 29.12.2020

from forecast_model import *
from ds import *
from store import *
from optable import *
from hbapi import HuobiServices as api
from util import *
import threading
import time
import argparse
import mail
import indicator
import math
from redis_cli import *
import orm
from orm import *
from orm import Schema as schema

#2017年11月1号为计算的起始点
zero_start = 1509465600
OneDay = 24 * 3600


class TimerLock:
    def __init__(self, key, value, interval):
        self.key_ = key
        self.val_ = value
        self.interval_ = interval
        pass
    def lock(self):
        g_redis.set(self.key_, self.val_, ex=self.interval_)
    def is_locked(self):
        val = g_redis.get(self.key_)
        if val is not None:
            log_debug("key %s is off"%self.key_)
            return True
        else:
            log_debug("key %s is on"%self.key_)
        return False

class RedularTask:
    def __init__(self, interval=600):
        self.interval_ = interval
        pass

def store_ls_ratio():
    #更新long short 信息: min一次
    interval = 300
    now = int(time.time())
    now = int(now/interval)*interval
    key = "store_ls_ratio_%d"%now
    store_lock = TimerLock(key, "val", interval)
    if store_lock.is_locked() :
        return 0
    optable = OpTable()
    log_info("======== going to long short info for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    for ct in Clist:
        optable.StoreLongShortRatio(ct, period=FMin)
    store_lock.lock()

def store_price():
    interval = 600
    store_lock = TimerLock("store_price", "val", interval)
    if store_lock.is_locked() :
        return 0
    store_handler = MysqlStore()
    optable = OpTable()
    #更新基础价格信息
    log_info("======== going to update price info for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    for ct in Clist:
        for duration in Dlist:
            store_handler.StorePrice(ct, duration, True)
            optable.StorePrice(ct, duration)
    store_lock.lock()

def store_ma():
    store_lock = TimerLock("store_ma", "val", 1800)
    if store_lock.is_locked() :
        return 0
    store_handler = MysqlStore()
    #更新ma信息
    log_info("======== going to update ma info for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    optable = OpTable()
    for ct in Clist:
        for duration in Dlist:
            store_handler.StoreMa(ct, duration, True)
            #optable.StoreMa(ct, duration, True)
    store_lock.lock()

def store_boll():
    store_lock = TimerLock("store_boll", "val", 1800)
    if store_lock.is_locked() :
        return 0
    store_handler = MysqlStore()
    #更新boll信息
    log_info("======== going to update boll info for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    optable = OpTable()
    for ct in Clist:
        for duration in Dlist:
            store_handler.StoreBoll(ct, duration)
            #optable.StoreBoll(ct, duration)
    store_lock.lock()

def store():
    store_ls_ratio()
    store_price()
    store_ma()
    store_boll()
    return 1

def sync_ma_data():
    #分别处理多个表
   #获取新表中缺失的数据的最后一位
   #提取老表中对应的数据
   #将新表中的数据插入到老表之中
   for currency_type in Clist:
       for duration in Dlist:
            data = orm.session.query(schema.MaInfo).filter(schema.MaInfo.currency_type==currency_type,
                    schema.MaInfo.period==duration,
                    ).order_by(schema.MaInfo.id.asc()).first()
            orm.session.commit()
            latest_ts = int(time.time())+ 3600
            if data is not None:
                latest_ts = data.id
            else:
                log_error("unexpected None data")
                #exit()

            lines = []
            if duration==Hour:
                lines = orm.session.query(schema.HourlyMa).filter(schema.HourlyMa.currency_type==currency_type, schema.HourlyMa.id < latest_ts).all()
            if duration==Quarter:
                lines = orm.session.query(schema.QuarterMa).filter(schema.QuarterMa.currency_type==currency_type, schema.QuarterMa.id < latest_ts).all()
            if duration==Day:
                lines = orm.session.query(schema.DailyMa).filter(schema.DailyMa.currency_type==currency_type, schema.DailyMa.id < latest_ts).all()
            if duration==Week:
                lines = orm.session.query(schema.WeeklyMa).filter(schema.WeeklyMa.currency_type==currency_type, schema.WeeklyMa.id < latest_ts).all()
            batch = 100
            for line in lines:
                nw_data = schema.MaInfo(id=line.id,
                        status=line.status,
                        currency_type=line.currency_type,
                        period=duration,
                        close=line.close,
                        delta=line.delta,
                        price_date=line.price_date)
                orm.session.add(nw_data)
                batch += 1
                if batch%100 == 0:
                    orm.session.commit()
            orm.session.commit()
   return 0

def sync_price_data():
    #分别处理多个表
   #获取新表中缺失的数据的最后一位
   #提取老表中对应的数据
   #将新表中的数据插入到老表之中
   for currency_type in Clist:
       for duration in Dlist:
            data = orm.session.query(schema.PriceInfo).filter(schema.PriceInfo.currency_type==currency_type,
                    schema.PriceInfo.period==duration,
                    ).order_by(schema.PriceInfo.id.asc()).first()
            orm.session.commit()
            latest_ts = int(time.time())
            if data is not None:
                latest_ts = data.id
            else:
                log_error("unexpected None data")
                exit()

            lines = []
            if duration==Hour:
                lines = orm.session.query(schema.HourlyPrice).filter(schema.HourlyPrice.currency_type==currency_type, schema.HourlyPrice.id < latest_ts).all()
            if duration==Quarter:
                lines = orm.session.query(schema.QuarterPrice).filter(schema.QuarterPrice.currency_type==currency_type, schema.QuarterPrice.id < latest_ts).all()
            if duration==Day:
                lines = orm.session.query(schema.DailyPrice).filter(schema.DailyPrice.currency_type==currency_type, schema.DailyPrice.id < latest_ts).all()
            if duration==Week:
                lines = orm.session.query(schema.WeeklyPrice).filter(schema.WeeklyPrice.currency_type==currency_type, schema.WeeklyPrice.id < latest_ts).all()
            batch = 100
            for line in lines:
                nw_data = schema.PriceInfo(id=line.id,
                        status=line.status,
                        currency_type=line.currency_type,
                        period=duration,
                        open=line.open,
                        close=line.close,
                        high=line.high,
                        low=line.low,
                        volume=line.amount,
                        price_date=line.price_date)
                orm.session.add(nw_data)
                batch += 1
                if batch%100 == 0:
                    orm.session.commit()
            orm.session.commit()
   return 0

def record():
    green_style="""<p><font color="green"> %s </font></p>"""
    red_style="""<p><font color="red"> %s </font></p>"""
    grey_style="""<p><font color="grey"> %s </font></p>"""
    recordLock = TimerLock("record", "val", 3600)
    if recordLock.is_locked():
        return 0
    keydata = indicator.Indicator()
    now  = int(time.time())
    now_hour=int(math.floor(now/3600))*3600
    subject="ls_ratio_info"
    content="<h2>*******Info********</h2>"

    #生成邮件内容
    valid_data = False
    count = 0
    special_count = 0
    #for ct in watchedList:
    for ct in Clist:
        accountLsRatio, lsRatio, diff, pp_percent, percent = keydata.long_short_ratio(ct)
        item = "ct=%s||accountLsr=%.2f||amountLsr=%.2f||lsr=%.2f||diff=%.2f||pp_percent=%.2f||percent=%.2f\n"%(ct, accountLsRatio, accountLsRatio*lsRatio, lsRatio, diff, pp_percent, percent)
        count += 1
        if accountLsRatio > 1.5:
            valid_data = True
            content = content + red_style%item
            special_count += 1
        elif percent > 75 or diff > 20:
            valid_data = True
            content = content + green_style%item
        elif percent < 25 or diff < -20:
            valid_data = True
            content = content + red_style%item
        else:
            content = content + grey_style%item
            count -= 1

    if valid_data :
        subject = "Carefull:" + subject
    else:
        subject = "Omit:" + subject
    mail.SendEmail(subject, content)
    recordLock.lock()
    return



class Ticker(threading.Thread):
    def __init__(self, threadId, name) :
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.status = -1
        pass

    def lsg(self):
        #小时级别的落水狗策略: 如果某一小时开盘价与收盘价格在2.95，那么会继续向该方向运动。
        #止损策略：1.6%
        #止盈策略：4.9%，任何时刻，相对最低点反弹1.6%，就按照实时价格进行止盈
        Clist=[BTC]
        start_list = [0, 10, 20, 30, 40]
        zero_start = int(time.time())
        for start_point in start_list:
            start_point = zero_start - 180 * OneDay + start_point * OneDay
            for ct in Clist:
                log_info("simulation start for ctype=%s || stg=lsg"%(ct))
                current_id = start_point
                currency_type = ct
                asset = assets[currency_type]
                asset.Reset(10000.0)
                printStart = False
                while current_id < now :
                    current_id += 3600
                    # price_list = GetPriceList(currency_type, duration=Hour, fetch_size=100, current_id)
                    # ma_list = GetMAList(currency_type, duration=Hour, fetch_size=100, current_id)
                    # enlarge_factor = 2.95

                    # 判断是否买入
                    # if price_list[0].close_ > (1+enlarge_factor/100.0) * price_list[0].open_:
                        # continue
                    # 判断是否卖出
        pass

    def heiTianE(self):
        #黑天鹅策略：上涨行情中，如果48H之内的下跌幅度满足特定数值，可以进行抄底。
        #Point1: 如何定义上涨行情：Ma5 > Ma10 > Ma20
        #Point2: 如何下跌幅度:
        #   * 下跌起始点（4H线的最高价和收盘价的均值）
        #   * 基准幅度：25%
        #   * 调整系数：最近五天上涨超过3%的天数的平均涨幅
        #point3: 仓位控制
        #   达到目标价位之后，开仓50%;
        #   每跌5%, 加仓10%
        now  = int(time.time())
        Clist=[BTC]
        start_list = [0, 30, 60]
        zero_start = (2019 - 1970) * 365 * OneDay
        for start_point in start_list:
            start_point = zero_start + start_point * OneDay
            for ct in Clist:
                log_info("heiTianE processing for ctyp=%s || start_point=%s"%(ct, timestamp2string(start_point)))
                current_id = start_point
                currency_type = ct
                asset = assets[currency_type]
                asset.Reset(10000.0)
                printStart = False
                while current_id < now :
                    current_id += 3600 * 24
                    price_list = GetPriceList(currency_type, Day, 100, current_id)
                    ma_list = GetMAList(currency_type, Day, 100, current_id)
                    merge_ma_list(price_list, ma_list)
                    price_list[0].IsMaUp()
        pass

    def run(self) :
        self.status = 0
        now  = int(time.time())
        Clist=[BTC]
        start_list = [0, 60, 120, 180, 240, 300, 360, 420]
        start_list = [180]
        for start_point in start_list:
            start_point = zero_start + start_point * OneDay
            for ct in Clist:
                log_info("processing for ctype of %s"%(ct))
                current_id = start_point
                currency_type = ct
                asset = assets[currency_type]
                asset.Reset(10000.0)
                printStart = False
                model = Model()
                while current_id < now :
                    current_id += 3600 * 24
                    boll_list = GetBollList(currency_type, Day, 30, current_id)
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
        last_hour = 0
        while True:
            start_time = int(time.time())
            store()
            interval = 60
            end_time = int(time.time())
            record()
            log_info("Store costs %d seconds, sleeping %d seconds for next round of store"%(end_time-start_time, interval))
            time.sleep(interval)
        pass


assets = {}
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description='runing as get/online/forecast'
    parser.add_argument("-g","--get",      action="store", help="get data from web",      dest="get",      nargs="?", type=str)
    parser.add_argument("-f","--forecast", action="store", help="forecasting of offline", dest="forecast", nargs="?", type=str)
    parser.add_argument("-o","--once", action="store", help="once ", dest="once", nargs="?", type=str)
    args = parser.parse_args()

    for ct in Clist:
        asset = Asset(ct, 10000.0)
        assets[ct] = asset

    if args.once:
        log_info("main is going to run as once")
        #sync_price_data()
        #sync_ma_data()
        print(api.get_user_interest_info("currency_based", var.BSV))

    if args.get:
        log_info("main is going to run as get")
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
