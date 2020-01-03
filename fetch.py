#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : fetch.py
# get price info from web
from hlog import *
from ds import *
from hbapi import HuobiServices as api

## get kline of diff duration and diff currency for diff depth
def GetHourlyKlines(currency_type="ht", depth=1):
    return get_current_kline(currency_type, "usdt", Hour, depth)
def GetQuarterKlines(currency_type="ht", depth=1):
    return get_current_kline(currency_type, "usdt", Quarter, depth)
def GetDailyKlines(currency_type="ht", depth=1):
    return get_current_kline(currency_type, "usdt", Day, depth)
def GetWeeklyKlines(currency_type="ht", depth=1):
    return get_current_kline(currency_type, "usdt", Week, depth)

def GetCurrentKline(currency_type="ht", duration="1min", depth=1):
    to_another = "usdt"
    return get_current_kline(currency_type, to_another, duration, depth)

#output: float
def GetCurrentPrice(currency_type):
    price_list = get_current_kline(currency_type, "usdt", "1min", 1)
    return price_list[0].open_

# 注意，第一个参数，一般都是Xusdt, 注意，这个顺序一般都是按照时间逆序排列。
# return list<Price>
def get_current_kline(currency_type="ht",to_another="usdt", period="1min", depth=1):
    resp = []
    currency_to_another=currency_type + to_another
    try:
        klines = api.get_kline(currency_to_another, period, depth)
    except:
        log_error("get kline failed for %s"%currency_to_another)
        return resp
    else:
        pass
    if not klines or klines["status"] != "ok":
        if klines:
            log_error("get kline resp status not ok, resp: %s"%(klines))
        return resp
    if len(klines["data"]) == 0:
        log_error("kline resp have no data for %s", currency_to_another)
        return resp
    price_list = klines["data"][0:depth]
    for price_unit in price_list:
        myprice = Price(currency_type)
        myprice.FromDict(price_unit)
        resp.append(myprice)
    return resp

##return float.
def get_open_price_today(currency_type):
    price_list = get_current_kline(currency_type, "usdt", "1day", 1)
    return price_list[0].open_
