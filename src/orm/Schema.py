# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, DateTime, Float, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BitfinexInfo(Base):
    __tablename__ = 'bitfinex_info'

    ts = Column(INTEGER(11), primary_key=True, nullable=False, comment='时间戳')
    symbol = Column(CHAR(10, 'utf8_bin'), primary_key=True, nullable=False)
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    long_volume = Column(DECIMAL(20, 8), comment='long')
    short_volume = Column(DECIMAL(20, 8), comment='short')
    long_ratio = Column(DECIMAL(20, 8), comment='多单占比')


class BlockInfo(Base):
    __tablename__ = 'block_info'

    ts = Column(INTEGER(11), primary_key=True, nullable=False, comment='时间戳')
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    symbol = Column(CHAR(10, 'utf8_bin'), primary_key=True, nullable=False)
    transactions = Column(DECIMAL(20, 4))
    active_addresss = Column(DECIMAL(20, 4))
    new_address = Column(DECIMAL(20, 4))
    adjusten_on_chain_volume = Column(DECIMAL(20, 4))
    miner_revenue = Column(DECIMAL(20, 4))
    addresss_with_balance_over_x = Column(DECIMAL(20, 4))


class CmeInfo(Base):
    __tablename__ = 'cme_info'

    ts = Column(INTEGER(11), primary_key=True, nullable=False, comment='时间戳')
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    symbol = Column(CHAR(10, 'utf8_bin'), primary_key=True, nullable=False)
    big_user_long_units = Column(DECIMAL(20, 4))
    big_user_short_units = Column(DECIMAL(20, 4))
    small_user_long_units = Column(DECIMAL(20, 4))
    small_user_short_units = Column(DECIMAL(20, 4))
    fund_user_long_units = Column(DECIMAL(20, 4))
    fund_user_short_units = Column(DECIMAL(20, 4))


class DailyGreedyFearIndex(Base):
    __tablename__ = 'daily_greedy_fear_index'

    ts = Column(INTEGER(11), primary_key=True, comment='时间戳')
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    greedy_fear_index = Column(INTEGER(10), server_default=text("50"))


class ExchangeInfo(Base):
    __tablename__ = 'exchange_info'
    __table_args__ = {'comment': '交易所相关信息：合约'}

    ts = Column(INTEGER(11), primary_key=True, nullable=False, comment='时间戳')
    symbol = Column(CHAR(10, 'utf8_bin'), primary_key=True, nullable=False)
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    exchange_name = Column(CHAR(20, 'utf8_bin'), primary_key=True, nullable=False, server_default=text("''"), comment='交易所名称')
    open_interest = Column(DECIMAL(20, 2), comment='合约持仓')
    user_long_ratio = Column(Float, nullable=False, server_default=text("0.5"))
    user_short_ratio = Column(Float, nullable=False, server_default=text("0.5"))
    amount_long_ratio = Column(Float, nullable=False, server_default=text("0.5"))
    amount_short_ratio = Column(Float, nullable=False, server_default=text("0.5"))
    fee_rate = Column(DECIMAL(20, 8), nullable=False, server_default=text("0.00000000"), comment='资金费率')
    boom_amont = Column(DECIMAL(20, 2), nullable=False, server_default=text("0.00"), comment='爆仓数据')


class Kline(Base):
    __tablename__ = 'kline'

    ts = Column(INTEGER(11), primary_key=True, nullable=False, comment='时间戳')
    exchange_name = Column(CHAR(20, 'utf8_bin'), primary_key=True, nullable=False, server_default=text("'okx'"), comment='交易所名称')
    symbol = Column(CHAR(20, 'utf8_bin'), primary_key=True, nullable=False)
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    interval = Column(ENUM('1H', '4H', '1D', '1W'), primary_key=True, nullable=False)
    o_price = Column(DECIMAL(20, 10))
    h_price = Column(DECIMAL(20, 10))
    l_price = Column(DECIMAL(20, 10))
    c_price = Column(DECIMAL(20, 10))
    vol = Column(DECIMAL(20, 4), comment='成交量:交易量，以张为单位')
    volCcy = Column(DECIMAL(20, 4), comment='成交量:交易量，以币为单位')
    volCcyQuote = Column(DECIMAL(20, 4), comment='成交量:交易量，以计价货币为单位')


class TestOrm(Base):
    __tablename__ = 'test_orm'

    ts = Column(INTEGER(11), primary_key=True, comment='时间戳')
    mtime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    uniq_id = Column(INTEGER(10), server_default=text("50"))
    name = Column(CHAR(10, 'utf8_bin'), nullable=False)
