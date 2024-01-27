#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from forecast_model import *
from ds import *
from store import *
from optable import *
from hbapi import HuobiServices as api
from util.convert import *
import threading
import time
import argparse
from iowapper import email
from iowapper.redis_cli import *
import indicator
import math
import orm
from orm import *
from orm import Schema as schema

#2017年11月1号为计算的起始点
zero_start = 1509465600
OneDay = 24 * 3600


def store_ls_ratio():
    #更新long short 信息: min一次
    interval = 300
    now = int(time.time())
    key = "store_ls_ratio_%d"%(int(now/interval)*interval)
    store_lock = TimerLock(key, "val", interval)
    if store_lock.is_locked() :
        return 0
    optable = OpTable()
    log_info("======== going to long short info for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    for ct in Clist:
        optable.StoreLongShortRatio(ct, period=FMin)
    store_lock.lock()

def store_interest_volume():
    #更新long short 信息: min一次
    interval = 1200
    now = int(time.time())
    if now%3600 < 600:
        return
    key = "store_interest_volume_%d"%(int(now/interval)*interval)
    store_lock = TimerLock(key, "val", interval)
    if store_lock.is_locked() :
        return 0
    optable = OpTable()
    log_info("======== going to store interest volume for currency_type=%s || Dlist=%s"%(Clist, Dlist))
    for ct in Clist:
        trueFalse = (now/3600%4 == 0)
        optable.StoreInterestVolume(ct, 48, var.Hour, trueFalse)
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
    store_interest_volume()
    store_price()
    store_ma()
    store_boll()
    return 1


if __name__ == '__main__':
    optable = OpTable()
    for ct in Clist:
        optable.StoreInterestVolume(ct, 48, var.Hour, True)
        pass

