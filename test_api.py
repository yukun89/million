#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : api.py
# Date              : 02.06.2019
# Last Modified Date: 02.06.2019
from hbapi import HuobiServices as api
from hbapi import BybtService as bybt
from hlog import *
from fetch import *
from indicator import *
import time
import datetime
#from orm import Schema as schema
#from orm import HbDb as huobi_db
from store import *

DEBUG = 1

# 交易记录，对应数据库的trade表
class TradeRecord:
    """
    oid             int         订单id
    type            string      交易对类型 "htusdt" "btcusdt" ...
    buy:            int         0 表示卖, 1 表示买
    usdt_amout      double      本次交易的 usdt 数量
    amout           double      本次交易数字货币的数量
    fee_amout       double      本次交易手续费. 买时为币的数量,卖时为usdt数量
    stat            int         订单状态。-1订单不存在 0正常 1已成交 2订单已取消
    tm              string      订单完成时间
    """
    def __init__(self,oid):
        self.oid = oid
        self.__cursor = MysqlSafeCursor()
        self.__need_save = True
        self.load()
    def __del__(self):
        if self.__need_save :
            self.save()
    def save(self):
        self.__need_save = False
        #tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        tm = self.tm
        sql = "insert into Trade values (%d,\'%s\',%d,%f,%f,%f,%d,\'%s\') on duplicate key update oid=%d,type=\'%s\',buy=%d,usdt_amout=%f,amout=%f,fee_amout=%f,stat=%d,tm=\'%s\'" % \
              (self.oid,self.type,self.buy,self.usdt_amout,self.amout,self.fee,self.stat,tm,
               self.oid,self.type,self.buy,self.usdt_amout,self.amout,self.fee,self.stat,tm)
        if self.__cursor.execute(sql) == False:
            log_error("[SQL EXECUTE] %s"%(sql))
    def load(self):
        sql = "select * from Trade where oid=%d" % self.oid
        if self.__cursor.execute(sql) == False:
            log_error("[SQL EXECUTE] %s"%(sql))
        res = self.__cursor.fetchone()
        if res != None:
            self.type = str(res[1])
            self.buy = int(res[2])
            self.usdt_amout = float(res[3])
            self.amout = float(res[4])
            self.fee = float(res[5])
            self.stat = int(res[6])
            self.tm = str(res[7])
        else:
            self.type = 'NULL'
            self.buy = 0
            self.usdt_amout = 0
            self.amout = 0
            self.fee = 0
            self.stat = -1
            self.tm = '2019-04-01 00:00:00'
    def delete(self):
        self.__need_save = False
        self.__cursor.execute("delete from Trade where oid=%d" % self.oid)

# get currency 'name': 总额，可交易额，冻结
def get_available_amount(name):
    trade = 0.0
    frozen = 0.0
    try:
        resp = api.get_balance()
    except:
            log_error("get balance faild!")
            return -1,0,0
    if not resp or resp["status"] != "ok":
        log_error("get balance resp status not ok")
        return -1,0,0
    if DEBUG:
        print("The resp[data][list] is ", resp["data"]["list"])
    for v in resp["data"]["list"]:
        if v["currency"] == name and v["type"] == "trade":
            trade = float(v["balance"])
        if v["currency"] == name and v["type"] == "frozen":
            frozen = float(v["balance"])
    return frozen+trade,trade,frozen


#========contract operation beggin=======#
#ret list: the supported contract"
def Get_supported_contract():
    '''
the element of the data looks like this:
{"symbol":"BTC","contract_code":"BTC190628","contract_type":"this_week","contract_size":100.000000000000000000,"price_tick":0.010000000000000000,"delivery_date":"20190628","create_date":"20190315","contract_status":1}
    '''
    result = []
    for i in range(2):
        try:
            resp = api.get_supported_contract()
        except:
            log_error("Failed to get_supported_contract for the %dth time" % i)
            continue
        if not resp or resp["status"] != "ok":
            log_error("no resp or status != ok for  get_supported_contract for the %dth time" % i)
            return result;
        if len(resp["data"]) == 0:
            log_error("not data for get_supported_contract for the %dth time" % i)
        return resp["data"]


def Get_contract_price(currency_type, contract_type):
    '''
@output:
    {"symbol":"BTC","contract_code":"BTC190705","contract_type":"next_week","high_limit":11101.490000000000000000000000000000000000,"low_limit":10440.870000000000000000000000000000000000}
    '''
    for i in range(2):
        try:
            resp = api.get_contract_price(currency_type, contract_type)
            if DEBUG:
                print(resp)
        except:
            print("resp")
            log_error("Failed to Get_contract_price for the %dth time" % i)
            continue
        if not resp or resp["status"] != "ok":
            log_error("no resp or status != ok for  Get_contract_price for the %dth time" % i)
            return result;
        if len(resp["data"]) == 0:
            log_error("not data for get_assets_info for the %dth time" % i)
        return resp["data"][0]
#========contract operation beggin=======#


#卖出：以市场价格卖出，x个币；限价卖出x个币
#买入：以市场价格买入，价值为y的币；限价买入x个币
def create_order(symbol, amout, long_short, price = 0):
    symbol = symbol+"usdt"
    if long_short == "buy":
        buy = 1
    elif long_short == "sell":
        buy = 0
    else:
        log_error("invalid parameter for long_short %s" % long_short)
        return
    """
    :arg amout: 只有在市场价买时才是usdt,其余均为ht
    :arg buy: 0 表示卖
              1 表示买
    :arg price: 默认0 以市场价交易
                非0 限价交易
    :return oid: -1 表示失败
    """
    log_info("create_order||amout=%f||buy=%d||price=%f"%(amout,buy,price))
    if buy:
        if price:
            exchange_type = "buy-limit"
        else:
            exchange_type = "buy-market"
    else:
        if price:
            exchange_type = "sell-limit"
        else:
            exchange_type = "sell-market"
    try:
        log_info("create_order||amout=%f||symbol=%s||exchange_type=%s||price=%f"%(amout,symbol, exchange_type, price))
        resp = api.send_order(amout,symbol,exchange_type,price)
    except:
        log_error("Create order failed!")
        return -1
    if not resp:
        log_error("Create order resp is null")
        return -1
    if resp["status"] != "ok":
        print(resp)
        log_error("Create order resp status false||err-code=%s" % resp["err-code"])
        return -1
    oid = int(resp["data"])
    while True:
        if get_order_info(oid, update = True) != -1:
            break
        time.sleep(1)
        log_error("Create order get order info failed")
    return oid


#返回订单是否完全成交,成交usdt数量,成交ht数量
# -1 异常
#  0 未成交
#  1 成交
def get_order_info(oid,update = False):
    """
    info["data"]中内容：
    字段               是否必须   类型      含义
    account-id	        true	long	账户 ID
    amount	            true	string	订单数量
    canceled-at	        false	long	订单撤销时间
    created-at	        true	long	订单创建时间
    field-amount        true	string	已成交数量
    field-cash-amount   true	string	已成交总金额
    field-fees	        true	string	已成交手续费（买入为币，卖出为钱）
    finished-at	        false	long	订单变为终结态的时间，不是成交时间，包含“已撤单”状态
    id	    true	long	订单ID
    price	true	string	订单价格
    source	true	string	订单来源	api
    state	true	string	订单状态	submitting , submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销
    symbol	true	string	交易对	btcusdt, ethbtc, rcneth ...
    type	true	string	订单类型	buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖, buy-ioc：IOC买单, sell-ioc：IOC卖单
    """
    try :
        info  = api.order_info(oid)
    except:
        log_error("get order info error||oid=%d" % oid)
        return -1,-1
    if info["status"] != "ok":
        log_warning("get order info resp status not ok||oid=%d" % oid)
        return -1,-1
    data = info["data"]
    print(data)
    if update :
        td_rcd = TradeRecord(oid)
        td_rcd.type = data["symbol"]
        if data["type"] in ("buy-market","buy-limit","buy-ioc"):
            td_rcd.buy = 1
        else:
            td_rcd.buy = 0
        td_rcd.usdt_amout = float(data["field-cash-amount"])
        td_rcd.amout = float(data["field-amount"])
        td_rcd.fee = float(data["field-fees"])
        if data["state"] == "filled":
            td_rcd.stat = 1
        elif data["state"] == "canceled":
            td_rcd.stat = 2
        else:
            td_rcd.stat = 0
        if td_rcd.stat == 1:
            td_rcd.tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(data["finished-at"]/1000))
        else:
            td_rcd.tm = "2019-04-01 00:00:00"
        td_rcd.save()
    if info["data"]["state"] == "filled":
        usdt_amout = float(info["data"]["field-cash-amount"])
        amout = float(info["data"]["field-amount"])
        fee_amout = float(data["field-fees"])
        if data["type"] in ("buy-market", "buy-limit", "buy-ioc"): #buy
            amout -= fee_amout
        else:     #sell
            usdt_amout -= fee_amout
        return 1,usdt_amout,amout
    else:
        return 0,-1

def cancel_order(order_id):
    log_info("cancel_order||oid=%d" % order_id)
    if order_id == 0: return 0
    try:
        resp = api.cancel_order(order_id)
    except:
        log_error("Cancel order faild||oid=%d"%order_id)
        return -1
    if not resp:
        log_error("cancel order resp is null")
        return -1
    if resp["status"] != "ok":
        log_warning("cancel order resp status false||err-code=%s" % resp["err-code"])
        return -1
    get_order_info(order_id,True)
    return 0

def refresh_trade(type):
    try:
        res = api.orders_list(type,"filled")
    except:
        return False
    if res['status'] != "ok":
        return False
    datas = res['data']
    for data in datas:
        if float(data['field-cash-amount']) > 5:
            if get_order_info(data['id'],True) != -1:
                print("oid:%d refresh success" % (data['id']))
    return True

def timestamp2date(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d", timeArray)

def get_yesterday_start_second():
    now  = int(time.time())
    daily_second = int(86400)
    yesterday_now = int(now - daily_second)
    yesterday = int(yesterday_now/daily_second)
    return yesterday * daily_second - 8 * 3600

#从daily_price表中获取当前价格，深度为depth
#return None of error
def get_daily_price(currency_type, depth=400, price_type="close"):
    save_daily_price(currency_type)
    expected_id = get_yesterday_start_second()
    full_currency_type = currency_type+"usdt"
    cursor = MysqlSafeCursor()
    cursor.execute("select id, %s from daily_price where currency_type='%s' order by price_date desc limit %d"%(price_type, full_currency_type, depth))
    id_price=cursor.fetchone()
    if expected_id != id_price[0]:
        log_error("The data is not updated yet(expected_id id is %d, while the newest in sql is %d), going to update data." % (expected_id, id_price[0]))
        return
    price_list = []
    while id_price != None:
        price_list.append(id_price[1])
        id_price=cursor.fetchone()
    print(price_list)
    return price_list

def calculate_MA_from_data(data_list, scale):
    res = []
    if len(data_list) == 0:
        return res
    for index in range(0, len(data_list)):
        res.append(sum(data_list[index:index + scale])/len(data_list[index:index + scale]))
    return res

# avg list-decimal: MA
def calculate_MA_line_by_currency(currency_type, scale):
    data = get_daily_price(currency_type,2000)
    avg = calculate_MA_from_data(data, scale)
    return avg

def calculate_MA_point_by_currency(currency_type, scale):
    MA_line = calculate_MA_line_by_currency(currency_type, scale)
    yesterday_MA = float(MA_line[0])
    print(yesterday_MA)
    open_price = get_open_price_today(currency_type)
    print(open_price)
    today_MA  = (yesterday_MA * scale + open_price)/(scale + 1)
    return today_MA


#Input:
##@cln (list):list
##@n (int):list
def EMA(cln,n):
    res = np.zeros(len(cln))
    res[0] = cln[0]
    for i in range(1,len(cln)):
        res[i] = 1.0*res[i-1]*(n-1)/(n+1) + 2.0*cln[i]/(n+1)
    return res

def EMA_n(p, c, n):
    return 1.0*p*(n-1)/(n+1) + 2.0*c/(n+1)

class MA:
    def __init__(self,cln,N):
        self.__N = N
        self.__wind = np.zeros(N)
        self.__wind_pos = 0
        self.val = np.zeros(len(cln))
        for i in range(0,len(cln)):
            desc_val = self.__wind[self.__wind_pos]
            n = min(i,N)
            self.val[i] = (1.0*self.val[i-1]*n - desc_val +cln[i])/min(i+1,N)
            self.__wind[self.__wind_pos] = cln[i]
            self.__wind_pos = (self.__wind_pos + 1) % self.__N

    def next(self,cl,update=False):
        desc_val = self.__wind[self.__wind_pos]
        n = min(len(self.val),self.__N)
        val_n = (1.0*self.val[-1]*n - desc_val + cl)/min(n+1,self.__N)
        if update:
            self.__wind[self.__wind_pos] = cl
            self.__wind_pos = (self.__wind_pos + 1) % self.__N
            self.val = np.append(self.val,val_n)
        return val_n
    def __getitem__(self, item):
        return self.val[item]

class MACD:
    def __init__(self,cln,S=14,L=26,M=9):
        self.__S = S
        self.__L = L
        self.__M = M
        self.__fast = EMA(cln,S)
        self.__slow = EMA(cln,L)
        self.dif = self.__fast-self.__slow
        self.dea = EMA(self.dif,M)

    def next(self,cl,update = False):
        fast_n = EMA_n(self.__fast[-1],cl,self.__S)
        slow_n = EMA_n(self.__slow[-1],cl,self.__L)
        dif_n = fast_n-slow_n
        dea_n = EMA_n(self.dea[-1],dif_n,self.__M)
        if update:
            self.__fast = np.append(self.__fast,fast_n)
            self.__slow = np.append(self.__slow,slow_n)
            self.dif = np.append(self.dif,dif_n)
            self.dea = np.append(self.dea,dea_n)
        return dif_n,dea_n

class ROC:
    def __init__(self,hi,lo,cl,N):
        self.__cl = cl
        n = min(len(hi),len(lo),len(cl))
        self.__ori_real_roc = np.zeros(n)
        for i in range(0,n):
            self.__ori_real_roc[i] = max(hi[i]-lo[i],hi[i]-cl[i-1],cl[i-1]-lo[i])
        self.__cl_ma = MA(cl,N)
        self.real_roc = MA(self.__ori_real_roc,N)
        self.ralt_val = self.real_roc.val/self.__cl_ma.val

    def next(self,hi,lo,cl,update=False):
        ori_real_roc = max(hi-lo,self.__cl[-1]-lo,hi-self.__cl[-1])
        real_roc = self.real_roc.next(ori_real_roc,update)
        cl_ma = self.__cl_ma.next(cl,update)
        ralt_roc = real_roc/cl_ma
        return ralt_roc,real_roc

def get_raw_price_data():
    #currency_types = ["btc", "omg", "zec", "dash", "ht", "etc", "eos", "bch", "ltc", "eth"]
    currency_types = ["btc"]
    for currency_type in currency_types:
        print("get currency of %s: total, trade,frozen" % currency_type)
        #print(get_available_amount(currency_type))
        print("price to usdt of %s" % currency_type)
        print("create order of %s" % currency_type)
        save_daily_price("btc")
        print("calculate_MA_line_by_currency:", calculate_MA_line_by_currency("xrp", 10))
        print("get_open_price_today", get_open_price_today("xrp"))
        print("calculate_MA_point_by_currency:", calculate_MA_point_by_currency("xrp", 10))

def save_daily_bias(currency_type):
    #stg1: 长时间上涨，目前处上涨行情中，乖离率大于30%, 如果仓位过高，考虑卖出
    calculate_MA_point_by_currency(currency_type, 10)
    return

if __name__ == '__main__':
    # print(Get_supported_contract())
    # print(Get_contract_price('xrp', 'next_week'))
    #get_raw_price_data()
    # print(bybt.get_account_long_short_ratio(symbol= 'xrp', timeType= 2))
    #print("API result:", get_current_long_short_info())
    #print("create order")
    #print("get order info")
    #print(get_order_info("35600450334"))
    #print(get_order_info("35600450334"))
    # print("API result:", bybt.get_amount_long_short_ratio(symbol= 'xrp', timeType= 3))
    # print("API result:", get_interest_amount_volume(BTC))
    monitor = Indicator()

    for ct in Clist:
        for i in range(0, 28):
            now = int(time.time())
            monitor.long_short_ratio(ct, now - i*3600*4)
            pass
    for ct in Clist:
        store_handler = MysqlStore()
        #store_handler.StoreLongShortRatio(ct, period=Quarter)
