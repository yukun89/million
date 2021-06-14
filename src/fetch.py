#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : fetch.py
# get price info from web

from hlog import *
from ds import *
from hbapi import HuobiServices as huobi
from hbapi import BybtService as bybt
import time

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

## buy sell info
def GetCurrentLongShortRatio(currency_type=BTC, duration=Hour, exName='Huobi'):
    return get_current_long_short_info(currency_type, duration, exName)

## buy sell info
def GetLongShortRatio(contract_type, ls_type, currency_type, period=Hour):
    return get_long_short_ratio(contract_type, ls_type, currency_type, period)

#output: float
def GetCurrentPrice(currency_type):
    price_list = get_current_kline(currency_type, "usdt", "1min", 1)
    return price_list[0].open_

#{"status":"ok","data":{"list":[{"buy_ratio":0.5000,"sell_ratio":0.4550,"locked_ratio":0.0450,"ts":1617285600000},{"buy_ratio":0.5070,"sell_ratio":0.4490,"locked_ratio":0.0440,"ts":1617285900000},{"buy_ratio":0.4920,"sell_ratio":0.4630,"locked_ratio":0.0450,"ts":1617286200000},{"buy_ratio":0.4920,"sell_ratio":0.4630,"locked_ratio":0.0450,"ts":1617286500000},{"buy_ratio":0.4780,"sell_ratio":0.4780,"locked_ratio":0.0440,"ts":1617286800000},{"buy_ratio":0.4780,"sell_ratio":0.4780,"locked_ratio":0.0440,"ts":1617287100000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617287400000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617287700000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617288000000},{"buy_ratio":0.5000,"sell_ratio":0.4580,"locked_ratio":0.0420,"ts":1617288300000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617288600000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617288900000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617289200000},{"buy_ratio":0.5130,"sell_ratio":0.4440,"locked_ratio":0.0430,"ts":1617289500000},{"buy_ratio":0.4920,"sell_ratio":0.4640,"locked_ratio":0.0440,"ts":1617289800000},{"buy_ratio":0.5270,"sell_ratio":0.4300,"locked_ratio":0.0430,"ts":1617290100000},{"buy_ratio":0.5070,"sell_ratio":0.4630,"locked_ratio":0.0300,"ts":1617290400000},{"buy_ratio":0.5070,"sell_ratio":0.4500,"locked_ratio":0.0430,"ts":1617290700000},{"buy_ratio":0.5210,"sell_ratio":0.4340,"locked_ratio":0.0450,"ts":1617291000000},{"buy_ratio":0.5280,"sell_ratio":0.4280,"locked_ratio":0.0440,"ts":1617291300000},{"buy_ratio":0.5280,"sell_ratio":0.4280,"locked_ratio":0.0440,"ts":1617291600000},{"buy_ratio":0.5280,"sell_ratio":0.4280,"locked_ratio":0.0440,"ts":1617291900000},{"buy_ratio":0.5280,"sell_ratio":0.4280,"locked_ratio":0.0440,"ts":1617292200000},{"buy_ratio":0.5280,"sell_ratio":0.4280,"locked_ratio":0.0440,"ts":1617292500000},{"buy_ratio":0.5210,"sell_ratio":0.4360,"locked_ratio":0.0430,"ts":1617292800000},{"buy_ratio":0.5400,"sell_ratio":0.4180,"locked_ratio":0.0420,"ts":1617293100000},{"buy_ratio":0.5350,"sell_ratio":0.4220,"locked_ratio":0.0430,"ts":1617293400000},{"buy_ratio":0.5270,"sell_ratio":0.4300,"locked_ratio":0.0430,"ts":1617293700000},{"buy_ratio":0.5130,"sell_ratio":0.4440,"locked_ratio":0.0430,"ts":1617294000000},{"buy_ratio":0.5130,"sell_ratio":0.4440,"locked_ratio":0.0430,"ts":1617294300000}],"symbol":"BTC","contract_code":"BTC-USDT"},"ts":1234231214}
def get_long_short_ratio(contract_type, ls_type, currency_type, period="60min"):
    #contract_type: dued, currency_based, usdt
    #ls_type: amount, account
    result = []
    contract_types = {"dued", "currency_based", "usdt"}
    ls_typs = {"amount", "account"}
    if contract_type not in contract_types:
        log_error("invalid contract_type %s"%contract_type)
        return result
    if ls_type not in ls_typs:
        log_error("invalid ls_types %s"%ls_type)
        return result

    resp = {}
    try:
        resp = huobi.get_long_short_ratio(contract_type, ls_type, currency_type, period)
    except Exception as e:
        log_error("Failed to get lsr for currency_type=%s. exception:%s"%(currency_type, e))
    else:
        log_debug("success get lsr for currency_type=%s"%currency_type)
    if not resp or resp["status"] != "ok" or not resp["data"]:
        if resp:
            log_error("http resp not ok for currency_type=%s||period=%s||type=%s||resp=%s"%(currency_type, period, ls_type, resp))
        return result
    data_list = resp["data"]["list"]
    for line in data_list:
        info = BuySellRatio(currency_type)
        info.buy_ratio_ = float(line["buy_ratio"])
        info.sell_ratio_ = float(line["sell_ratio"])
        info.id_ = int(int(line["ts"])/1000)
        info.contract_type_ = contract_type
        info.ls_type_ = ls_type
        result.append(info)
    return result

#{'status': 'ok', 'data': {'symbol': 'BTC', 'tick': [{'volume': 7923.030839231547, 'amount_type': 2, 'ts': 1623657600000}, {'volume': 7937.367931491199, 'amount_type': 2, 'ts': 1623654000000}, {'volume': 7969.345135261478, 'amount_type': 2, 'ts': 1623650400000}, {'volume': 7957.421153581986, 'amount_type': 2, 'ts': 1623646800000}, {'volume': 8026.149411272458, 'amount_type': 2, 'ts': 1623643200000}, {'volume': 7969.546314819047, 'amount_type': 2, 'ts': 1623639600000}, {'volume': 7851.254320294865, 'amount_type': 2, 'ts': 1623636000000}, {'volume': 7946.295159144407, 'amount_type': 2, 'ts': 1623632400000}, {'volume': 7873.162419443697, 'amount_type': 2, 'ts': 1623628800000}, {'volume': 7914.976116741984, 'amount_type': 2, 'ts': 1623625200000}, {'volume': 7987.491191885733, 'amount_type': 2, 'ts': 1623621600000}, {'volume': 7859.054012660813, 'amount_type': 2, 'ts': 1623618000000}, {'volume': 8210.305444887119, 'amount_type': 2, 'ts': 1623614400000}, {'volume': 8235.683148852515, 'amount_type': 2, 'ts': 1623610800000}, {'volume': 8168.026424265784, 'amount_type': 2, 'ts': 1623607200000}, {'volume': 8274.651084853136, 'amount_type': 2, 'ts': 1623603600000}, {'volume': 8334.840398220387, 'amount_type': 2, 'ts': 1623600000000}, {'volume': 8363.459351944195, 'amount_type': 2, 'ts': 1623596400000}, {'volume': 8346.987945095592, 'amount_type': 2, 'ts': 1623592800000}, {'volume': 8370.338037596921, 'amount_type': 2, 'ts': 1623589200000}, {'volume': 8425.681794749617, 'amount_type': 2, 'ts': 1623585600000}, {'volume': 8422.311155577789, 'amount_type': 2, 'ts': 1623582000000}, {'volume': 8368.962955100307, 'amount_type': 2, 'ts': 1623578400000}, {'volume': 8470.50090260321, 'amount_type': 2, 'ts': 1623574800000}, {'volume': 8514.216457580267, 'amount_type': 2, 'ts': 1623571200000}, {'volume': 8563.671388101982, 'amount_type': 2, 'ts': 1623567600000}, {'volume': 8678.228386945226, 'amount_type': 2, 'ts': 1623564000000}, {'volume': 8675.439570608922, 'amount_type': 2, 'ts': 1623560400000}, {'volume': 8602.556163346751, 'amount_type': 2, 'ts': 1623556800000}, {'volume': 8400.206702585476, 'amount_type': 2, 'ts': 1623553200000}, {'volume': 8369.030378623629, 'amount_type': 2, 'ts': 1623549600000}, {'volume': 8330.215642601555, 'amount_type': 2, 'ts': 1623546000000}, {'volume': 8381.74452462337, 'amount_type': 2, 'ts': 1623542400000}, {'volume': 8441.548375543187, 'amount_type': 2, 'ts': 1623538800000}, {'volume': 8443.966502561929, 'amount_type': 2, 'ts': 1623535200000}, {'volume': 8469.12784674057, 'amount_type': 2, 'ts': 1623531600000}, {'volume': 8408.839593687282, 'amount_type': 2, 'ts': 1623528000000}, {'volume': 8400.505251664907, 'amount_type': 2, 'ts': 1623524400000}, {'volume': 8425.400460228322, 'amount_type': 2, 'ts': 1623520800000}, {'volume': 8473.926772824794, 'amount_type': 2, 'ts': 1623517200000}, {'volume': 8428.089420900482, 'amount_type': 2, 'ts': 1623513600000}, {'volume': 8388.417624209904, 'amount_type': 2, 'ts': 1623510000000}, {'volume': 8364.442825847633, 'amount_type': 2, 'ts': 1623506400000}, {'volume': 8426.474790603732, 'amount_type': 2, 'ts': 1623502800000}, {'volume': 8613.261751613683, 'amount_type': 2, 'ts': 1623499200000}, {'volume': 8715.800130688527, 'amount_type': 2, 'ts': 1623495600000}, {'volume': 8735.125364630036, 'amount_type': 2, 'ts': 1623492000000}, {'volume': 8715.430935756769, 'amount_type': 2, 'ts': 1623488400000}], 'contract_code': 'BTC-USD'}, 'ts': 1623659709782}

def get_interest_volume(contract_type, currency_type, period='60min'):
    #contract_type: dued, currency_based, usdt
    result = []
    contract_types = {"dued", "currency_based", "usdt"}
    if contract_type not in contract_types:
        log_error("invalid contract_type %s"%contract_type)
        return result

    resp = {}
    try:
        resp = huobi.get_interest_volume(contract_type, currency_type, period)
    except Exception as e:
        log_error("Failed to get interest volume for currency_type=%s. exception:%s"%(currency_type, e))
    else:
        log_debug("success get interest volume for currency_type=%s"%currency_type)
    if not resp or resp["status"] != "ok" or not resp["data"]:
        if resp:
            log_error("http resp not ok for currency_type=%s||period=%s||resp=%s"%(currency_type, period, resp))
        return result
    data_list = resp["data"]["tick"]
    for line in data_list:
        info = TradeInfo(currency_type)
        info.id_ = int(int(line["ts"])/1000)
        info.volume_ = float(line["volume"])
        result.append(info)
    return result




#{"code":"0","msg":"success","data":{"longRatioList":[62.0,63.0,63.0,62.0,63.0,62.0,62.0,62.0,62.0,62.0,62.0,63.0,63.0,63.0,63.0,63.0,63.0,63.0,62.0,63.0,63.0,64.0,62.0,62.0,64.0,66.0,65.0,65.0,65.0,66.0],"shortRatioList":[36.0,35.0,35.0,36.0,35.0,36.0,36.0,36.0,36.0,36.0,36.0,35.0,35.0,35.0,35.0,35.0,35.0,35.0,36.0,36.0,36.0,35.0,36.0,36.0,35.0,33.0,34.0,34.0,34.0,33.0],"longShortRatioList":[1.72,1.8,1.8,1.72,1.8,1.72,1.72,1.72,1.72,1.72,1.72,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.72,1.75,1.75,1.83,1.72,1.72,1.83,2.0,1.91,1.91,1.91,2.0],"dateList":[1612750200000,1612750500000,1612750800000,1612751100000,1612751400000,1612751700000,1612752000000,1612752300000,1612752600000,1612752900000,1612753200000,1612753500000,1612753800000,1612754100000,1612754400000,1612754700000,1612755000000,1612755300000,1612755600000,1612755900000,1612756200000,1612756500000,1612756800000,1612757100000,1612757400000,1612757700000,1612758000000,1612758300000,1612758600000,1612758900000],"lockedRatioList":[2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,1.0,1.0,1.0,2.0,2.0,1.0,1.0,1.0,1.0,1.0,1.0]},"success":true}}}
#duplicated bybt
def get_current_long_short_info(currency_type="btc", period=Hour, exName='Huobi', retry = 1):
    resp = []
    timeType = byTimeTypeMap[period]

    #1 获取人数多空比
    try :
        account_resp = bybt.get_account_long_short_ratio(currency_type, timeType, exName)
    except Exception as e:
        log_error("Bybt API ERROR get buy sell account ratio for currency_type=%s || period=%s || timeType=%d || account_resp=%s || exName=%s || exception=%s"%(currency_type, period, timeType, account_resp, exName, str(e)))
    else:
        log_info("success get account long short ratio %s"%account_resp)
    ##1.1结果合法性校验
    if not account_resp or account_resp["success"] != True or not account_resp["data"]:
        if account_resp:
            log_error("http resp not ok for currency_type=%s || period=%s || account_resp=%s"%(currency_type, period, account_resp))
        return resp
    account_data = account_resp["data"]
    length = len(account_data["dateList"])
    long_length = len(account_data["longRatioList"])
    short_length = len(account_data["shortRatioList"])
    if length == 0 or long_length !=  length or short_length != length:
        log_error("account_data invalid for currency_type=%s || period=%s || account_data=%s || length=%d || longRatioLength=%d || shortRatioLength=%d", currency_type, period, account_data, length, long_length, short_length)
        return resp

    #2 获取仓位多空比
    try :
        amount_resp=bybt.get_amount_long_short_ratio(currency_type, timeType, exName)
    except Exception as e:
        log_error("Bybt API ERROR get buy sell amount ratio for currency_type=%s || period=%s || timeType=%d || account_resp=%s || exName=%s || exception=%s"%(currency_type, period, timeType, amount_resp, exName, str(e)))
    else:
        log_info("success get amount long short ratio %s"%amount_resp)
    if not amount_resp or amount_resp["success"] != True or not amount_resp["data"]:
        if amount_resp:
            log_error("http resp not ok for currency_type=%s || period=%s || amount_resp=%s"%(currency_type, period, amount_resp))
        return resp

    ## 2.1结果合法性校验
    amount_data = amount_resp["data"]
    length2 = len(amount_data["dateList"])
    long_length = len(amount_data["longRatioList"])
    short_length = len(amount_data["shortRatioList"])
    if length2 == 0 or long_length !=  length2 or short_length != length2:
        log_error("amount data invalid for currency_type=%s || period=%s || amount_data=%s || length=%d || longRatioLength=%d || shortRatioLength=%d", currency_type, period, amount_data, length, long_length, short_length)
        return resp
    if account_data["dateList"][0] != amount_data["dateList"][0] or length != length2:
        if retry <= 3:
        #如果时间序列正好不等，那么重新获取一次
            sleep_time = 60 * retry * retry
            time.sleep(sleep_time)
            log_warn("Invalid data from web. sleep %d min and try again"%(retry*retry))
            return get_current_long_short_info(currency_type, period, retry+1)
        else:
            log_warn("Invalid data from web for more than three times")


    for index in range(length):
        lsInfo = LongShortRatio(currency_type)
        lsInfo.account_long_short_ratio_ = float(account_data["longShortRatioList"][index])
        lsInfo.amount_long_short_ratio_ = float(amount_data["longShortRatioList"][index])
        lsInfo.id_ = int(account_data["dateList"][index])/1000
        resp.append(lsInfo)

    return resp

#获取合约持仓量
#def get_amount_volume(symbol):
#not used
def get_interest_amount_volume(currency_type):
    result = {}
    try:
        resp = bybt.get_amount_volume(currency_type)
    except Exception as e:
        log_error("Failed to get interest amount volume for currency_type=%s"%currency_type)
    else:
        log_debug("success get interest amount volume for currency_type=%s"%currency_type)
    if not resp or resp["success"] != True or not resp["data"]:
        if resp:
            log_error("http resp for interest not ok for currency_type=%s || resp=%s"%(currency_type, resp))

    for line in resp["data"]:
        market = line["exchangeName"]
        volume = line["openInterestAmount"]
        result[market] = float(volume)
    return result

# 注意，第一个参数，一般都是Xusdt, 注意，这个顺序一般都是按照时间逆序排列。
# return list<Price>
def get_current_kline(currency_type="ht",to_another="usdt", period="1min", depth=1):
    resp = []
    currency_to_another=currency_type + to_another
    try:
        klines = huobi.get_kline(currency_to_another, period, depth)
    except Exception as e:
        log_error("huobi API ERROR get kline failed for %s"%currency_to_another)
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
