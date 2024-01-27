#!/bin/bash
#sqlacodegen --tables long_short_ratio,boll,ma_info,price_info,hourly_price,daily_price,quarter_price,weekly_price,hourly_ma,quarter_ma,daily_ma,weekly_ma --outfile=./Schema.py mysql+pymysql://ykhuang:m159357M.@localhost:3306/huobi?charset=utf8;
sqlacodegen --tables block_info,cme_info,daily_greedy_index,kline,exchange_info,bitfinex_info --outfile=./Schema.py mysql+pymysql://rw_user_huangyukun:'2022CpHykMillion.'@10.0.0.11:3306/million?charset=utf8;
