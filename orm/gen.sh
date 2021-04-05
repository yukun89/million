#!/bin/bash
#tables=('long_short_ratio', 'boll')
sqlacodegen --tables long_short_ratio,boll --outfile=./Schema.py mysql+pymysql://ykhuang:m159357M.@localhost:3306/huobi?charset=utf8;
