# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, DateTime, Enum, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Boll(Base):
    __tablename__ = 'boll'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    duration = Column(CHAR(10), primary_key=True, nullable=False)
    price_date = Column(DateTime, primary_key=True, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    mid = Column(DECIMAL(20, 8))
    upper = Column(DECIMAL(20, 8))
    lower = Column(DECIMAL(20, 8))


class LongShortRatio(Base):
    __tablename__ = 'long_short_ratio'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    market = Column(CHAR(10), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    account_long_short_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_long_short_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_volume = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_buy_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_sell_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    account_buy_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    account_sell_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    contract_type = Column(Enum('dued', 'currency_based', 'usdt'), primary_key=True, nullable=False, server_default=text("'usdt'"))
