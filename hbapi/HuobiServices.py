#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

from .Utils import *

'''
Market data API
'''
##############contact begin ##############
DEBUG = 1
#https://api.hbdm.com/api/v1/contract_contract_info
valid_currency_type = {'btc', 'xrp'}
valid_contract_type = {'this_week', 'next_week', 'quarter'}
def validate_currency_type(currency_type):
    res = currency_type in valid_currency_type
    return res
def validate_contract_type(contract_type):
    res = contract_type in valid_contract_type
    return res

CONTACT_URL = "https://api.hbdm.com/"
def get_supported_contract():
    url="api/v1/contract_contract_info"
    full_url = CONTACT_URL + url
    params = {}
    return http_get_request(full_url, params)


def get_contract_price(currency_type, contract_type):
    '''
@input:
https://api.hbdm.com/api/v1/contract_price_limit?symbol=BTC&contract_type=next_week
- contract_type: this_week, next_week, quarter
@output:
    eg:
    {"status":"ok","data":[{"symbol":"BTC","contract_code":"BTC190705","contract_type":"next_week","high_limit":11101.490000000000000000000000000000000000,"low_limit":10440.870000000000000000000000000000000000}],"ts":1561656650362}
    '''
    if DEBUG:
        print("comming to get_contract_price(%s, %s)" % (currency_type, contract_type))
    if validate_currency_type(currency_type) == False or validate_contract_type(contract_type) == False:
        log_error("Invalid input for currency_type:[%s], contract_type:[%s]" % (currency_type, contract_type))
        return
    url = "api/v1/contract_price_limit?symbol=%s&contract_type=%s" % (currency_type, contract_type)
    full_url = CONTACT_URL + url;
    if DEBUG:
        print(full_url)
    params = {}
    return http_get_request(full_url, params)

##############contact end   ##############

# 获取KLine
def get_kline(symbol, period, size=150):
    """
    :param symbol
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: 可选值： [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# 获取marketdepth
def get_depth(symbol, type):
    """
    :param symbol
    :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}
    
    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)


# 获取tradedetail
def get_trade(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)

# Tickers detail
def get_tickers():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/market/tickers'
    return http_get_request(url, params)

# 获取merge ticker
def get_ticker(symbol):
    """
    :param symbol: 
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail/merged'
    return http_get_request(url, params)


# 获取 Market Detail 24小时成交量数据
def get_detail(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)

# 获取  支持的交易对
def get_symbols(long_polling=None):
    """

    """
    params = {}
    if long_polling:
        params['long-polling'] = long_polling
    path = '/v1/common/symbols'
    return api_key_get(params, path)

# Get available currencies
def get_currencies():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/v1/common/currencys'

    return http_get_request(url, params)

# Get all the trading assets
def get_trading_assets():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/v1/common/symbols'

    return http_get_request(url, params)

'''
Trade/Account API
'''


def get_accounts():
    """
    :return: 
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)

# 获取当前账户资产
def get_balance():
    """
    :param acct_id
    :return:
    """
    acct_id = ACCOUNT_ID
    
    if not acct_id:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id'];

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)


# 下单

# 创建并执行订单
def send_order(amount, symbol,_type,price=0,source="api"):
    """
    :param amount: 
    :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
    :param symbol: 
    :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param price: 
    :return: 
    """

    acct_id = ACCOUNT_ID
    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


# 撤销订单
def cancel_order(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)

# 查询某个订单
def order_info(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


# 查询某个订单的成交明细
def order_matchresults(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


# 查询当前委托、历史委托
def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    
    :param symbol: 
    :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol,
              'states': states}

    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/orders'
    return api_key_get(params, url)


# 查询当前成交、历史成交
def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    
    :param symbol: 
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol}

    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/matchresults'
    return api_key_get(params, url)

# 查询所有当前帐号下未成交订单
def open_orders(symbol,side='',size=10):
    """
    :param symbol: 
    :return: 
    """
    account_id = ACCOUNT_ID
    params = {}
    url = "/v1/order/openOrders"
    if symbol:
        params['symbol'] = symbol
    if account_id:
        params['account-id'] = account_id
    if side:
        params['side'] = side
    if size:
        params['size'] = size
    
    return api_key_get(params, url)

# 批量取消符合条件的订单
def cancel_open_orders(symbol,side='',size=10):
    """
    :param symbol: 
    :return: 
    """
    account_id = ACCOUNT_ID
    params = {}
    url = "/v1/order/orders/batchCancelOpenOrders"
    if symbol:
        params['symbol'] = symbol
    if account_id:
        params['account-id'] = account_id
    if side:
        params['side'] = side
    if size:
        params['size'] = size
    
    return api_key_post(params, url)

# 申请提现虚拟币
def withdraw(address, amount, currency, fee=0, addr_tag=""):
    """

    :param address_id: 
    :param amount: 
    :param currency:btc, ltc, bcc, eth, etc ...(火币Pro支持的币种)
    :param fee: 
    :param addr-tag:
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {'address': address,
              'amount': amount,
              "currency": currency,
              "fee": fee,
              "addr-tag": addr_tag}
    url = '/v1/dw/withdraw/api/create'

    return api_key_post(params, url)

# 申请取消提现虚拟币
def cancel_withdraw(address_id):
    """

    :param address_id: 
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

    return api_key_post(params, url)


'''
借贷API
'''

# 创建并执行借贷订单


def send_margin_order(amount, source, symbol, _type, price=0):
    """
    :param amount: 
    :param source: 'margin-api'
    :param symbol: 
    :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param price: 
    :return: 
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print ('get acct_id error.%s' % e)
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": 'margin-api'}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)

# 现货账户划入至借贷账户


def exchange_to_margin(symbol, currency, amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol": symbol,
              "currency": currency,
              "amount": amount}

    url = "/v1/dw/transfer-in/margin"
    return api_key_post(params, url)

# 借贷账户划出至现货账户


def margin_to_exchange(symbol, currency, amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol": symbol,
              "currency": currency,
              "amount": amount}

    url = "/v1/dw/transfer-out/margin"
    return api_key_post(params, url)

# 申请借贷
def get_margin(symbol, currency, amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol": symbol,
              "currency": currency,
              "amount": amount}
    url = "/v1/margin/orders"
    return api_key_post(params, url)

# 归还借贷
def repay_margin(order_id, amount):
    """
    :param order_id: 
    :param amount: 
    :return: 
    """
    params = {"order-id": order_id,
              "amount": amount}
    url = "/v1/margin/orders/{0}/repay".format(order_id)
    return api_key_post(params, url)

# 借贷订单
def loan_orders(symbol, currency, start_date="", end_date="", start="", direct="", size=""):
    """
    :param symbol: 
    :param currency: 
    :param direct: prev 向前，next 向后
    :return: 
    """
    params = {"symbol": symbol,
              "currency": currency}
    if start_date:
        params["start-date"] = start_date
    if end_date:
        params["end-date"] = end_date
    if start:
        params["from"] = start
    if direct and direct in ["prev", "next"]:
        params["direct"] = direct
    if size:
        params["size"] = size
    url = "/v1/margin/loan-orders"
    return api_key_get(params, url)


# 借贷账户详情,支持查询单个币种
def margin_balance(symbol):
    """
    :param symbol: 
    :return: 
    """
    params = {}
    url = "/v1/margin/accounts/balance"
    if symbol:
        params['symbol'] = symbol
    
    return api_key_get(params, url)



#=======合约多空比信息
#交割合约
#curl "https://api.hbdm.com/api/v1/contract_elite_account_ratio?symbol=BTC&period=60min"

#usdt 合约
#curl "https://api.hbdm.com/linear-swap-api/v1/swap_elite_account_ratio?contract_code=BTC-USDT&period=60min"

#币本位合约
def get_long_short_ratio(contract_type, ls_type, symbol, period):
    urls={"dued_account_url":"/api/v1/contract_elite_account_ratio",
            "dued_amount_url":"/api/v1/contract_elite_position_ratio",
            "usdt_account_url":"/linear-swap-api/v1/swap_elite_account_ratio",
            "usdt_amount_url":"/linear-swap-api/v1/swap_elite_position_ratio",
            "currency_based_account_url":"/swap-api/v1/swap_elite_account_ratio",
            "currency_based_amount_url":"/swap-api/v1/swap_elite_position_ratio"}
    params = {}
    swap_type="USDT"
    if contract_type=="currency_based":
        swap_type="USD"
    params["contract_code"]="%s-%s"%(symbol,swap_type)
    params["period"] = period
    params["symbol"] = symbol
    url_key = "%s_%s_url"%(contract_type, ls_type)
    url = urls[url_key]

    full_url = HBDM_URL + url
    return http_get_request(full_url, params)
"""
{
    "status": "ok",
    "data": {
        "symbol": "BTC",
        "tick": [
            {
                "volume": 2124.0000000000000000,
                "amount_type": 1,
                "ts": 1603695600000,
                "value": 27771.93720000000000000000000000000000000
            }
        ],
        "contract_code": "BTC-USDT"
    },
    "ts": 1603695899986
}
"""
def get_interest_volume(contract_type, symbol, period, size=48):
    urls={"usdt":"/linear-swap-api/v1/swap_his_open_interest",
            "dued":"/api/v1/contract_his_open_interest",
            "currency_based":"/swap-api/v1/swap_his_open_interest"}
    params = {}
    swap_type="USDT"
    if contract_type=="currency_based":
        swap_type="USD"
    params["contract_code"]="%s-%s"%(symbol,swap_type)
    params["period"] = period
    params["amount_type"] = 2#1 张；2币
    
    return http_get_request(full_url, params)

def get_user_asset_info(contract_type, symbol):
    urls={"usdt":"/linear-swap-api/v1/swap_account_position_info",
            "dued":"",
            "currency_based":""}
    params = {}
    swap_type="USDT"
    if contract_type =="currency_based":
        swap_type="USD"
    params["contract_code"]="%s-%s"%(symbol,swap_type)
    url_key = "%s"%(contract_type)
    url = urls[url_key]
    return api_key_post(HBDM_URL, url, params)
