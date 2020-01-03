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
    def IsGrow():
        if self.open_ > self.close_ * (1 + 0.015) :
            return 1
        elif self.open_ < self.close_ * (1 - 0.015) :
            return -1
        else:
            return 0

    def IsUpNeedle():
        bigger = max(self.open_, self.close_)
        return self.high_ > bigger * (1 + 0.07)

    def IsDownNeedle():
        smaller = min(self.open_, self.close_)
        return self.low_ < smaller * (1 - 0.07)
