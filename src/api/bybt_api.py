#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *

DEBUG = 0
# 获取人数多空比
# https://fapi.bybt.com/api/tradingData/accountLSRatio?exName=Huobi&symbol=XRP&type=0&timeType=3

BYBT_URL="https://fapi.bybt.com"
def get_account_long_short_ratio(symbol, timeType=2, exName='Huobi'):
    """
    :param symbol
    :param timeType: 可选值： [五分钟，1小时，4小时，12小时，24小时] 分别对应 [3, 2, 1, 4, 5]
    :return:
    """
    inputType = '0'
    if exName == 'Binance':
        inputType = '1'
    elif exName == 'Okex':
        inputType = '-1'

    params = {'symbol': symbol,
              'timeType': timeType,
              'exName': exName,
              'type': inputType}

    url = BYBT_URL + '/api/tradingData/accountLSRatio'
    if DEBUG == 1:
        print("DEBUG get_account_long_short_ratio: url=%s || params=%s"%(url, params))
    return http_get_request(url, params)

def get_amount_long_short_ratio(symbol, timeType=2, exName='Huobi'):
    """
    :param symbol
    :param timeType: 可选值： [五分钟，1小时，4小时，12小时，24小时] 分别对应 [3, 2, 1, 4, 5]
    :return:
    """
    inputType = '0'
    if exName == 'Binance':
        inputType = '1'
    elif exName == 'Okex':
        inputType = '-1'
    params = {'symbol': symbol,
              'timeType': timeType,
              'exName': exName,
              'type': inputType}

    url = BYBT_URL + '/api/tradingData/positionLSRatio'
    if DEBUG == 1:
        print("DEBUG get_amount_long_short_ratio: url=%s || params=%s"%(url, params))
    return http_get_request(url, params)

#https://fapi.bybt.com/api/openInterest/pc/info?symbol=BTC
def get_amount_volume(symbol):
    url_prefix = "/api/openInterest/pc/info"
    symbol = symbol.upper()
    params = {'symbol': symbol}
    url = BYBT_URL + url_prefix
    if DEBUG == 1:
        print("DEBUG get_amount_long_short_ratio: url=%s || params=%s"%(url, params))
    return http_get_request(url, params)

if __name__ == '__main__':
    DEBUG=1
    print(get_account_long_short_ratio('BTC', timeType=2, exName='Huobi'))
    print(get_amount_long_short_ratio('BTC', timeType=2, exName='Huobi'))
    print(get_amount_volume('BTC'))
