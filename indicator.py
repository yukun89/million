#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : mmonitor.py

import time
import util
from var import *
import store
from redis_cli import *
from hlog import *

class Indicator():
    def __init__(self):
        pass
    #计算当前货币的供需比以及处于的百分位
    def long_short_ratio(self, ct="", ts=0):
        log_info("handle ls ratio for ct=%s"%ct)
        lsRatio = 1.0
        percent = 50.0
        diff = 0.0
        now = int(time.time())
        if ts != 0:
            now = ts
        ratios = []
        diffs = []
        percents = []

        currency_type = ct
        for market in Markets:
            store_handler = store.MysqlStore()
            lsRatioList = store_handler.GetLSRatio(currency_type, market, ts)
            lsSize = len(lsRatioList)
            if lsSize < 4:
                continue
            thisRatio = lsRatioList[0].get_long_short_ratio()
            one = lsRatioList[1].get_long_short_ratio()
            two = lsRatioList[2].get_long_short_ratio()
            diff = (thisRatio*2/(one+two)- 1) * 100

            bigger = 0
            smaller = 0
            for lsRatio in lsRatioList:
                thatRatio = lsRatio.get_long_short_ratio()
                if thisRatio > thatRatio:
                    bigger += 1
                else:
                    smaller += 1
            #获取最近30day多空比的分位数
            percent = bigger*100.0 / lsSize

            ratios.append(thisRatio)
            diffs.append(diff)
            percents.append(percent)
            log_debug("Indicator lsr-single: ct=%s || dt=%s || LsRatio(1.0)=%.2f || diff(100)=%.2f || percent(100)=%.2f || markets=%s"%(currency_type, util.timestamp2string(now), thisRatio, diff, percent, market))

        if len(ratios) == 0:
            log_warn("empty data for ls ration: ct=%s"%currency_type)
            return lsRatio, diff, percent


        ratio = sum(ratios)/len(ratios)
        diff= sum(diffs)/len(diffs)
        percent = sum(percents)/len(percents)
        log_debug("Indicator lsr-total: ct=%s || dt=%s || LsRatio(1.0)=%.2f || diff(100)=%.2f || percent(100)=%.2f || markets=%d"%(currency_type, util.timestamp2string(now), ratio, diff, percent, len(ratios)))
        return ratio, diff, percent

