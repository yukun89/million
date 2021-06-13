#!/bin/bash
sqlacodegen --tables long_short_ratio,boll,ma_info,price_info,hourly_price,daily_price,quarter_price,weekly_price,hourly_ma,quarter_ma,daily_ma,weekly_ma --outfile=./Schema.py mysql+pymysql://ykhuang:m159357M.@localhost:3306/huobi?charset=utf8;
