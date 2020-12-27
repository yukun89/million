from hlog import *
import time
import datetime

Hour="60min"
Quarter="4hour"
Day="1day"
Week="1week"

#Duration的list
Dlist = (Hour, Quarter, Day, Week)

BTC="btc"
EOS="eos"
OMG="omg"
DASH="dash"
HT="ht"
ETC="etc"
ETH="eth"
LTC="ltc"
XRP="xrp"

#Currency的List
Clist = (BTC, EOS, OMG, DASH, HT, ETC, ETH, LTC, XRP)

#Step的list
Slist = (5, 10, 20, 30, 60, 90, 120)
Duration2ptable = {Hour: "hourly_price", Quarter: "quarter_price", Day: "daily_price", Week: "weekly_price"}
Duration2ktable = {Hour: "hourly_kline", Quarter: "quarter_kline", Day: "daily_kline", Week: "weekly_kline"}
Duration2second = {"1min":60,"5min":300,"15min":900,"30min":1800, Hour:3600, Quarter:14400, Day:86400, Week:604800,"30day":2592000}

def timestamp2dstring(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d")
        return str1
    except Exception as e:
        print(e)
    return ''

class Order:
    #switch = -1: buy, switch = 1: sell
    def __init__(self, switch, currency_type, vol, price, created_tid):
        self.buy_sell_ = switch
        self.ct_ = currency_type
        self.vol_ = vol
        self.created_tid_ = created_tid
        self.price_ = price
        self.status_ = 0

class Asset:
    def __init__(self, currency_type, usdt = 10000.0):
        self.ct_ = currency_type
        self.usdt_ = usdt
        self.ct_volume_ = 0
        self.lose_ = 0.002
        self.buy_list_ = []
        self.sell_list_ = []

    def Reset(self, usdt = 10000.0):
        self.usdt_ = usdt
        self.ct_volume_ = 0
        self.lose_ = 0.002
        self.buy_list_ = []
        self.sell_list_ = []


    def Buy(self, volume, dprice, amount = 0, tid = 0, buy_model=""):
        price = float(dprice)
        if self.usdt_ <= 100:
            return
        if amount > 0:
            if amount > self.usdt_:
                amount = self.usdt_
            volume = amount * 1.0 / price
        consume = (1+self.lose_) * price * volume
        if consume > self.usdt_:
            consume = self.usdt_
            volume = consume / ((1+self.lose_) * price)
        self.ct_volume_ += volume
        self.usdt_ -= (1+self.lose_) * price * volume
        total = self.ct_volume_ * price + self.usdt_
        percent = (1 - self.usdt_/total) * 100
        order = Order(-1, self.ct_, volume, price, tid)
        self.buy_list_.append(order)
        log_info("buy %-2s %-4s  @%s@ || vol %6.2f || price %6.4f || usdt %6.2f || percent %02d"%(buy_model, self.ct_, timestamp2dstring(tid), self.ct_volume_, price, self.usdt_, percent))
        pass

    def Sell(self, volume, dprice, amount = 0, tid = 0, sell_model = ""):
        price = float(dprice)
        if amount > 0:
            volume = amount * 1.0 /price
            if volume > self.ct_volume_:
                volume = self.ct_volume_
        amount = (1-self.lose_) * price * volume
        if amount < 1:
            return
        self.ct_volume_ -= volume
        self.usdt_ += amount
        total = self.ct_volume_ * price + self.usdt_
        percent = (1 - self.usdt_/total) * 100
        order = Order(1, self.ct_, volume, price, tid)
        self.sell_list_.append(order)
        log_info("sell %-2s %-4s @%s@ || vol %6.2f || price %6.4f || usdt %6.2f || percent %02d"%(sell_model, self.ct_, timestamp2dstring(tid), self.ct_volume_, price, self.usdt_, percent))
        pass

    def Percent(self, price):
        total = self.ct_volume_ * price + self.usdt_
        return 1 - self.usdt_ / total

    def Total(self, price):
        total = self.ct_volume_ * float(price) + self.usdt_
        return total

    def Output(self, dprice, prefix):
        price = float(dprice)
        log_info("[%s] %s: vol %.4f || price %.2f || usdt %08.2f || total %.2f || bs %d-%d"%(prefix, self.ct_, self.ct_volume_, price, self.usdt_, self.usdt_ + price * self.ct_volume_, len(self.buy_list_), len(self.sell_list_)))
        return

class Price:
    def __init__(self, currency_type):
        self.currency_type_ = currency_type
        self.id_ = int(0)
        self.open_ = float(1.0)
        self.close_ = float(1.0)
        self.high_ = float(1.0)
        self.low_ = float(1.0)
        self.vol_ = float(1.0)
        self.amount_ = float(1.0)
        self.count_ = int(1)
        self.avg_ = float(1.0)
        #技术指标
        self.ma5_ = float(1.0)
        self.ma10_ = float(1.0)
        self.ma20_ = float(1.0)
        self.ma30_ = float(1.0)
        self.ma60_ = float(1.0)
        self.ma90_ = float(1.0)
        self.ma120_ = float(1.0)

        self.boll_high_ = float(1.0)
        self.boll_low_ = float(1.0)
        self.boll_mid_ = float(1.0)
        pass

    def ToDict(self):
        data = {
                "id" : self.id_,
                "amount" : self.amount_,
                "open" : self.open_,
                "close" : self.close_,
                "high" : self.high_,
                "low" : self.low_,
                "count" : self.count_,
                "vol" : self.vol_
                }
        return data

    def FromDict(self, data):
        self.id_ = int(data["id"])
        self.amount_ = float(data["amount"])
        self.open_ = float(data["open"])
        self.close_ = float(data["close"])
        self.high_ = float(data["high"])
        self.low_ = float(data["low"])
        self.count_ = int(data["count"])
        self.vol_ = int(data["vol"])
        pass

    #单日股价特征：有效上涨、有效下跌、向上插针、向下插针
    def IsGrow(self):
        if self.open_ > self.close_ * (1 + 0.015) :
            return 1
        elif self.open_ < self.close_ * (1 - 0.015) :
            return -1
        else:
            return 0

    def CalculateMaSellVolFactor(self):
        factor = 0
        if self.ma10_ < self.ma20_ * (1-0.015) :
            factor = 1
        elif self.ma5_ < self.ma10_ * (1-0.015) :
            factor = 0.5
        return factor

    def CalculateMaBuyVolFactor(self):
        factor = 0
        if self.ma10_ > self.ma20_ * (1+0.015) and self.ma10_ < self.ma20_ * 1.10 :
            factor = 0.4
        elif self.ma5_ > self.ma10_ * (1+0.015) and self.ma5_ < self.ma10_ * 1.10 :
            factor = 0.2
        return factor

    def CallBackFactor(self):
        if self.high_ > 1.05 * self.close_:
            return (1.0* self.high_  - self.close_)/self.high_
        return 0


    def IsUpNeedle(self):
        bigger = max(self.open_, self.close_)
        return self.high_ > bigger * (1 + 0.07)

    def IsDownNeedle(self):
        smaller = min(self.open_, self.close_)
        return self.low_ < smaller * (1 - 0.07)

    def merge_mpb(self, p, b):
        #把ma与price和bollmerge起来
        if self.id_ != p.id_ or self.id_ != b.id_:
            return False
        self.high_ = float(p.high_)
        self.low_ = float(p.low_)
        self.open_ = float(p.open_)
        self.close_ = float(p.close_)

        self.boll_mid_ = float(b.boll_mid_)
        self.boll_high_ = float(b.boll_high_)
        self.boll_low_ = float(b.boll_low_)
        return True


class TradeParam:
    def __init__(self):
        self.factor = 0.0
        self.price = 0.0
        self.level = 0
        self.model = ""
        pass

