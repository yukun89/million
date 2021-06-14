#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 15:48:13 2018

@author: zhaobo
"""

from HuobiDMService import HuobiDM
from pprint import pprint

#### input huobi dm url
URL = "https://api.hbdm.com/"

####  input your access_key and secret_key below:
ACCESS_KEY = "831ed9ab-bgrdawsdsd-91ee1a48-6d171" #TODO
SECRET_KEY = "0de8fba9-00295ca0-4a84d354-6bde7" #TODO
#ACCESS_KEY = "6ea7d226-1hrfj6yhgg-218ab01b-04cf3" #TODO
#SECRET_KEY = "04813819-46ba4ac1-87f28dd1-d8dc6" #TODO


dm = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)

#### another account:
#dm2 = HuobiDM(URL, "ANOTHER ACCOUNT's ACCESS_KEY", "ANOTHER ACCOUNT's SECRET_KEY")




#%%  market data api ===============

def test_api():
    print (u' 获取合约信息 ')
    '''
{'data': [{'contract_code': 'BTC190927',
           'contract_size': 100.0,
           'contract_status': 1,
           'contract_type': 'quarter',
           'create_date': '20190614',
           'delivery_date': '20190927',
           'price_tick': 0.01,
           'symbol': 'BTC'}],
 'status': 'ok',
 'ts': 1561779420436}
    '''
    res = dm.get_contract_info(symbol="BTC", contract_type="quarter")
    pprint (type(res))
    pprint (res)
    '''
{'data': [{'contract_code': 'BTC190705',
           'contract_size': 100.0,
           'contract_status': 1,
           'contract_type': 'this_week',
           'create_date': '20190621',
           'delivery_date': '20190705',
           'price_tick': 0.01,
           'symbol': 'BTC'}],
 'status': 'ok',
 'ts': 1561781755701}
    '''
    #pprint (dm.get_contract_info(contract_code="BTC190705"))

    print (u' 获取合约指数信息 ')
    '''
{'data': [{'index_price': 11423.373333333333,
           'index_ts': 1561781796048,
           'symbol': 'BTC'}],
 'status': 'ok',
 'ts': 1561781800729}
    '''
    #pprint (dm.get_contract_index("BTC"))

    print (u' 获取合约最高限价和最低限价 ')
    '''
{'data': [{'contract_code': 'BTC190927',
           'contract_type': 'quarter',
           'high_limit': 12692.23,
           'low_limit': 11255.39,
           'symbol': 'BTC'}],
 'status': 'ok',
 'ts': 1561781865349}
    '''
    #pprint (dm.get_contract_price_limit(symbol='BTC', contract_type='this_week'))
    '''
{'data': [{'contract_code': 'BTC190705',
           'contract_type': 'this_week',
           'high_limit': 12099.86,
           'low_limit': 11230.66,
           'symbol': 'BTC'}],
 'status': 'ok',
 'ts': 1561798759521}
    '''
    #pprint (dm.get_contract_price_limit(contract_code='BTC190705'))

    print (u' 获取当前可用合约总持仓量 ')
    '''
{'data': [{'amount': 16796.144516956818,
           'contract_code': 'BTC190927',
           'contract_type': 'quarter',
           'symbol': 'BTC',
           'volume': 2031665.0}],
 'status': 'ok',
 'ts': 1561799022253}
    '''
    #pprint (dm.get_contract_open_interest(symbol='BTC', contract_type='quarter'))
    #pprint (dm.get_contract_open_interest(contract_code='BTC190705'))

    print (u' 获取行情深度数据 ')
    #pprint (dm.get_contract_depth(symbol='BTC_CW', type='step1'))

    print (u' 获取K线数据 ')
    #这个interface的返回值，数组坐标小对应的时间早
    '''其中某个元素的信息如下, 数组最末的是最近一小时的数据
    {'amount': 885.8070436772243,
           'close': 11779.47,
           'count': 2484,
           'high': 11809.91,
           'id': 1561798800,
           'low': 11676.45,
           'open': 11724.05,
           'vol': 104058}
    '''
    pprint (dm.get_contract_kline(symbol='BTC_CW', period='60min', size=10))

    print (u' 获取聚合行情 ')
    #pprint (dm.get_contract_market_merged('BTC_CW'))

    print (u' 获取市场最近成交记录 ')
    #pprint (dm.get_contract_trade('BTC_CW'))

    print (u' 批量获取最近的交易记录 ')
    #pprint (dm.get_contract_batch_trade(symbol='BTC_CW', size=3))



    #%% trade / account api  ===============

    print (u' 获取用户账户信息 ')
    pprint (dm.get_contract_account_info())
    #pprint (dm.get_contract_account_info("BTC"))
    return

    print (u' 获取用户持仓信息 ')
    pprint (dm.get_contract_position_info())
    pprint (dm.get_contract_position_info("BTC"))

    print (u' 合约下单 ')
    #pprint(dm.send_contract_order(symbol='', contract_type='', contract_code='BTC190705', 
                            #client_order_id='', price=10000, volume=1, direction='sell',
                            #offset='open', lever_rate=5, order_price_type='limit'))


    print (u' 合约批量下单 ')
    orders_data = {'orders_data': [
                   {'symbol': 'BTC', 'contract_type': 'quarter',  
                    'contract_code':'BTC190705',  'client_order_id':'', 
                    'price':10000, 'volume':1, 'direction':'sell', 'offset':'open', 
                    'leverRate':5, 'orderPriceType':'limit'},
                   {'symbol': 'BTC','contract_type': 'quarter', 
                    'contract_code':'BTC190705', 'client_order_id':'', 
                    'price':20000, 'volume':2, 'direction':'sell', 'offset':'open', 
                    'leverRate':5, 'orderPriceType':'limit'}]}
    #pprint(dm.send_contract_batchorder(orders_data))


    print (u' 撤销订单 ')
    #pprint(dm.cancel_contract_order(symbol='BTC', order_id='42652161'))

    print (u' 全部撤单 ')
    #pprint(dm.cancel_all_contract_order(symbol='BTC'))

    print (u' 获取合约订单信息 ')
    #pprint(dm.get_contract_order_info(symbol='BTC', order_id='42652161'))

    print (u' 获取合约订单明细信息 ')
    #pprint(dm.get_contract_order_detail(symbol='BTC', order_id='42652161', order_type=1, created_at=1542097630215))

    print (u' 获取合约当前未成交委托 ')
    #pprint(dm.get_contract_open_orders(symbol='BTC'))

    print (u' 获取合约历史委托 ')
    #pprint (dm.get_contract_history_orders(symbol='BTC', trade_type=0, type=1, status=0, create_date=7))

if __name__=='__main__':
   test_api()




