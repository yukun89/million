#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : mmonitor.py

import time
from util.convert import *
from var import *
import store
from iowapper.redis_cli import *
from hlog import *
import orm
from orm import *
import var

class Indicator():
    def __init__(self):
        pass
    #计算当前货币的供需比以及处于的百分位
    def long_short_ratio(self, ct="", ts=0, period=var.FMin, all=False):
        log_info("handle ls ratio for ct=%s"%ct)
        lsRatio = 1.0
        percent = 50.0
        pp_percent = 50.0
        diff = 0.0
        now = int(time.time())
        if ts != 0:
            now = ts
        account_ratios= []
        amount_ratios = []
        ratios = []
        diffs = []
        percents = []
        pp_percents = []

        currency_type = ct
        market = 'Huobi'
        types = ['usdt']
        if all:
            types = var.ContractTypes
        for contract_type in types:
            store_handler = store.MysqlStore()
            lsRatioList = store_handler.GetLSRatio(contract_type, currency_type, market, ts, period)
            lsSize = len(lsRatioList)
            if lsSize < 4:
                log_warn("no enough data for lsr data. contract_type=%s || currency_type=%s"%(contract_type, currency_type))
                continue
            thisAccountRatio = orm.get_account_lsr(lsRatioList[0])
            thisAmountRatio = orm.get_amount_lsr(lsRatioList[0])
            thisRatio = orm.get_lsr(lsRatioList[0])
            history10 = list(map(lambda x:orm.get_lsr(x), lsRatioList[0:10]))
            ma10 = sum(history10)/len(history10)
            diff = (thisRatio/ma10 - 1) * 100

            bigger = 0
            smaller = 0
            max_ratio = -1.0
            min_ratio = 10.0
            for lsRatio in lsRatioList:
                thatRatio = get_lsr(lsRatio)
                max_ratio= max(max_ratio, thatRatio)
                min_ratio = min(min_ratio, thatRatio)
                if thisRatio > thatRatio:
                    bigger += 1
                else:
                    smaller += 1
            percent = bigger*100.0 / lsSize
            pp_percent = (thisRatio - min_ratio)/(max_ratio - min_ratio) * 100

            amount_ratios.append(thisAmountRatio)
            account_ratios.append(thisAccountRatio)
            ratios.append(thisRatio)
            diffs.append(diff)
            percents.append(percent)
            pp_percents.append(pp_percent)
            size = len(lsRatioList)
            log_debug("Indicator lsr-single: ct=%s || dt=%s || LsRatio(1.0)=%.2f || diff(100)=%.2f || pp_percent(100)=%.2f || percent = %.2f|| contract_type=%s || lsr_size=%d"%(currency_type, timestamp2string(now), thisRatio, diff, pp_percent, percent, contract_type, size))

        if len(ratios) == 0:
            log_warn("empty data for ls ration: ct=%s"%currency_type)
            return 1.0, lsRatio, diff, pp_percent, percent


        amount_ratio = sum(amount_ratios)/len(amount_ratios)
        account_ratio = sum(account_ratios)/len(account_ratios)
        ratio = sum(ratios)/len(ratios)
        diff= sum(diffs)/len(diffs)
        percent = sum(percents)/len(percents)
        pp_percent = sum(pp_percents)/len(pp_percents)
        log_debug("Indicator lsr-total: ct=%s || dt=%s || LsRatio(1.0)=%.2f || diff(100)=%.2f || pp_percent = %.2f || percent(100)=%.2f"%(currency_type, timestamp2string(now), ratio, diff, pp_percent, percent))
        return account_ratio, ratio, diff, pp_percent, percent

