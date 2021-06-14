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


class DailyMa(Base):
    __tablename__ = 'daily_ma'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    close = Column(DECIMAL(20, 8))
    delta = Column(INTEGER(11), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class DailyPrice(Base):
    __tablename__ = 'daily_price'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    open = Column(DECIMAL(20, 8))
    high = Column(DECIMAL(20, 8))
    low = Column(DECIMAL(20, 8))
    close = Column(DECIMAL(20, 8))
    amount = Column(DECIMAL(20, 8))
    price_date = Column(DateTime, primary_key=True, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class HourlyMa(Base):
    __tablename__ = 'hourly_ma'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    close = Column(DECIMAL(20, 8))
    delta = Column(INTEGER(11), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class HourlyPrice(Base):
    __tablename__ = 'hourly_price'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    open = Column(DECIMAL(20, 8))
    high = Column(DECIMAL(20, 8))
    low = Column(DECIMAL(20, 8))
    close = Column(DECIMAL(20, 8))
    amount = Column(DECIMAL(20, 8))
    price_date = Column(DateTime, primary_key=True, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class LongShortRatio(Base):
    __tablename__ = 'long_short_ratio'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    market = Column(CHAR(10), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    amount_volume = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_buy_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    amount_sell_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    account_buy_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    account_sell_ratio = Column(DECIMAL(20, 8), server_default=text("-1.00000000"))
    contract_type = Column(Enum('dued', 'currency_based', 'usdt'), primary_key=True, nullable=False, server_default=text("'usdt'"))


class MaInfo(Base):
    __tablename__ = 'ma_info'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    period = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("'60min'"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    close = Column(DECIMAL(20, 8))
    delta = Column(INTEGER(11), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class PriceInfo(Base):
    __tablename__ = 'price_info'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    period = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("'60min'"))
    open = Column(DECIMAL(20, 8))
    high = Column(DECIMAL(20, 8))
    low = Column(DECIMAL(20, 8))
    close = Column(DECIMAL(20, 8))
    volume = Column(DECIMAL(20, 8))
    price_date = Column(DateTime, primary_key=True, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class QuarterMa(Base):
    __tablename__ = 'quarter_ma'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    close = Column(DECIMAL(20, 8))
    delta = Column(INTEGER(11), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class QuarterPrice(Base):
    __tablename__ = 'quarter_price'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    open = Column(DECIMAL(20, 8))
    high = Column(DECIMAL(20, 8))
    low = Column(DECIMAL(20, 8))
    close = Column(DECIMAL(20, 8))
    amount = Column(DECIMAL(20, 8))
    price_date = Column(DateTime, primary_key=True, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class WeeklyMa(Base):
    __tablename__ = 'weekly_ma'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    close = Column(DECIMAL(20, 8))
    delta = Column(INTEGER(11), primary_key=True, nullable=False)
    price_date = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class WeeklyPrice(Base):
    __tablename__ = 'weekly_price'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("0"))
    currency_type = Column(CHAR(10), primary_key=True, nullable=False)
    open = Column(DECIMAL(20, 8))
    high = Column(DECIMAL(20, 8))
    low = Column(DECIMAL(20, 8))
    close = Column(DECIMAL(20, 8))
    amount = Column(DECIMAL(20, 8))
    price_date = Column(DateTime, primary_key=True, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
