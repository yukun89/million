FMin="5min"

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
BCH="bch"
BSV="bsv"
ADA="ada"
LINK="link"
BAND="band"
UNI="uni"

#Currency的List
Clist = (BTC, EOS, OMG, DASH, HT, ETC, ETH, LTC, XRP, BCH, BSV, ADA, LINK, BAND, UNI)

Duration2ptable = {Hour: "hourly_price", Quarter: "quarter_price", Day: "daily_price", Week: "weekly_price"}
Duration2ktable = {Hour: "hourly_ma", Quarter: "quarter_ma", Day: "daily_ma", Week: "weekly_ma"}
Duration2second = {"1min":60,"5min":300,"15min":900,"30min":1800, Hour:3600, Quarter:14400, Day:86400, Week:604800,"30day":2592000}

byTimeTypeMap = {FMin: 3, Hour: 2, Quarter: 1, Day:5}

Markets=['Huobi', 'Binance', 'Okex']

ContractTypes=['usdt', 'dued', 'currency_based']
LsTypes=['amount', 'account']
