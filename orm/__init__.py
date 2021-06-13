# __init__.py
from .HbDb import *
from .Schema import *

DbSession = create_db_scoped_session()
session = DbSession()

def get_account_lsr(long_short_ratio):
    return long_short_ratio.account_buy_ratio/long_short_ratio.account_sell_ratio

def get_amount_lsr(long_short_ratio):
    return long_short_ratio.amount_buy_ratio/long_short_ratio.amount_sell_ratio

def get_lsr(long_short_ratio):
    return get_amount_lsr(long_short_ratio)/get_account_lsr(long_short_ratio)

