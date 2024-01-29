# __init__.py
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    print('orm __init__ run as main with path %s' % sys.path)
    from Schema import *

    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://rw_user_huangyukun:2022CpHykMillion.@localhost:3306/million')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    #test insert
    orm_item = TestOrm(ts=0,uniq_id=1,name='zhangsan')
    # 添加到session:
    session.add(orm_item)
    # 提交即保存到数据库:
    session.commit()
    #test query

else:
    #from .HbDb import *
    from .Schema import *
    engine = create_engine('mysql+pymysql://rw_user_huangyukun:2022CpHykMillion.@localhost:3306/million')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


    def get_account_lsr(long_short_ratio):
        return long_short_ratio.account_buy_ratio / long_short_ratio.account_sell_ratio


    def get_amount_lsr(long_short_ratio):
        return long_short_ratio.amount_buy_ratio / long_short_ratio.amount_sell_ratio


    def get_lsr(long_short_ratio):
        return get_amount_lsr(long_short_ratio) / get_account_lsr(long_short_ratio)
