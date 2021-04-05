#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
pymysql.install_as_MySQLdb()
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import BigInteger, BIGINT, Text, Date, DateTime, SmallInteger, String, Integer,CHAR,Float
import copy
from .Schema import *

def _create_engine(user='ykhuang', password='m159357M.', host='127.0.0.1', port=3306, db='huobi', autocommit=False, pool_recycle=60, charset='utf8'):
    engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=%s&use_unicode=1' % (user, password, host, port, db, charset),
                           pool_size=10,
                           max_overflow=-1,
                           pool_recycle=pool_recycle,
                           connect_args={'connect_timeout': 3,
                                         'autocommit': 1 if autocommit else 0} )
    return engine

def create_db_scoped_session():
    _engine = _create_engine()
    session = scoped_session(sessionmaker())
    session.configure(bind=_engine, autocommit=False,
                      autoflush=False, expire_on_commit=False)
    return session

DbSession = create_db_scoped_session()
session = DbSession()

def add():
    #数据库增删改查操作
    lsr1 = LongShortRatio(id=-1, currency_type='btc', market='huobi', amount_buy_ratio=float(1.2))

    #add
    session.add(copy.deepcopy(lsr1))
    session.commit()

def query():
    data = session.query(LongShortRatio).filter(LongShortRatio.market=='huobi', LongShortRatio.contract_type=='usdt').order_by(LongShortRatio.id.desc()).limit(30).all()
    session.commit()
    print(data[0].id)
    #select

#add()

