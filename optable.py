#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#read and write info from/to mysql
from hlog import *
from ds import *
from fetch import *
import pymysql
import time
import cmath
from decimal import Decimal
import orm
from orm import *
from orm import Schema as schema
import copy
import var


#def getLatestIdOfPrice(currency_type, duration, table, delta = 0, only_active=True):


#对mysql中的业务数据进行读写:主要是Get/Store方法
class OpTable:
    def __init__(self):
        pass

    #从数据库中获取boll指标
    def GetBollList(self, currency_type, duration, fetch_size=20, now_id = 0):
        if now_id == 0:
            now_id=time.time()
        interval = Duration2second[duration]
        data = orm.session.query(schema.Boll).filter(schema.Boll.currency_type==currency_type,
                schema.Boll.duration==duration,
                schema.Boll.id <= now_id).order_by(schema.Boll.id.desc()).limit(fetch_size)
        orm.session.commit()
        length=len(data)
        begin = data[0].id
        end = data[length-1].id
        if length != (end - begin)/interval + 1:
            log_error("boll data is not lost. begin=%d||end=%d||duration=%s||length=%d"%(begin, end, duration, length))
            data.clear()
        return data

    #从数据库中获取MA指
    def GetMAList(self, currency_type, duration, fetch_size, now_id = 0):
        if now_id == 0:
            now_id=time.time()
        interval = Duration2second[duration]
        data = orm.session.query(schema.MaInfo).filter(schema.MaInfo.currency_type==currency_type,
                schema.MaInfo.duration==duration,
                schema.MaInfo.id <= now_id).order_by(schema.MaInfo.id.desc()).limit(fetch_size)
        orm.session.commit()
        length=len(data)
        begin = data[0].id
        end = data[length-1].id
        if length != (end - begin)/interval + 1:
            log_error("ma data is not lost. begin=%d||end=%d||duration=%s||length=%d"%(begin, end, duration, length))
            data.clear()
        return data

    #降序排列: 获取now_id 之前的数据
    def GetPriceList(self, currency_type, duration, fetch_size, now_id = 0):
        if now_id <= 0 :
            now_id = time.time()
        interval = Duration2second[duration]
        price_info_lines = orm.session.query(schema.PriceInfo).filter(schema.PriceInfo.currency_type==currency_type,
                schema.PriceInfo.period==duration,
                schema.price_list.id<=now_id).order_by(schema.PriceInfo.id.desc()).limit(fetch_size).all()
        orm.session.commit()

        begin = price_info_lines[0].id
        end = price_info_lines[len(price_info_lines)-1].id
        real_size = len(price_info_lines)
        if real_size != (end - begin)/interval + 1:
            log_error("price data is lost. begin=%d||end=%d||currency_type=%s||period=%s"(begin, end, currency_type, duration))
            price_info_lines.clear()

        return price_info_lines


    def StoreBoll(self, currency_type, duration):
        interval=Duration2second[duration]
        latest_status1_line = orm.session.query(schema.BollInfo).filter(schema.PriceInfo.currency_type==currency_type,
                schema.PriceInfo.period==duration,
                schema.PriceInfo.status==1).order_by(schema.BollInfo.id.desc()).limit(1).first()
        orm.session.commit()
        status1_latest_id = latest_status1_line
        now = time.time()
        to_fill_size = int((now - status1_latest_id)/interval)

        latest_status0_lines = orm.session.query(schema.BollInfo).filter(schema.PriceInfo.currency_type==currency_type,
                schema.PriceInfo.period==duration,
                schema.PriceInfo.status==0).all()
        orm.session.commit()
        status0_latest_ids = {}
        for line in latest_status0_lines:
            status0_latest_ids.add(line.id)


        fetch_size = to_fill_size + step -1
        price_list = self.GetPriceList(currency_type, duration, fetch_size)
        price_list = sorted(price_list, key=lambda price:price.id)
        now  = int(time.time())
        interval = Duration2second[duration]
        if len(price_list) != fetch_size:
            log_warn("UpdateBoll no enough data in table %s of currency_type=%s || step=%d. get %d items while %d items is expected. from %s to %s"%(ptable, currency_type, step, len(price_list), fetch_size, timestamp2string(price_list[0].id), timestamp2string(price_list[-1].id)));
        for i in range(step-1, len(price_list)):
            array = price_list[i+1 - step : i+1]
            close_price_list = [x.close for x in array]
            avg = sum(close_price_list)/step
            variance = sum([(avg - x)*(avg - x) for x in close_price_list])/step
            std_variance = variance ** (Decimal(0.5))
            upper = avg + 2 * std_variance
            lower = avg - 2 * std_variance
            status = 0
            ts = price_list[i].id
            if now - ts > interval:
                status = 1
            boll_info = schema.Boll(id=ts,
                    status=status,
                    period=duration,
                    currency_type=currency_type,
                    mid=avg,
                    upper=upper,
                    lower=lower,
                    price_date=timestamp2string(ts))
        return 0

    #以当前需要更新的索引为1，如果需要更新10个M5均线，那么需要获取14条数据（最后一条数据是需要用10-11-12-13-14来更新）
    def StoreMa(self, currency_type, duration, refresh = True):
        log_info("request_in StoreMa: ct=%s || duration=%s ", currency_type, duration)
        now  = int(time.time())
        interval = Duration2second[duration]

        #Step的list
        Slist = (5, 10, 20, 30, 60)

        #获取最新的有效id
        latest_line = orm.session.query(schema.MaInfo).filter(schema.MaInfo.currency_type==currency_type,
                schema.MaInfo.period==duration,
                schema.MaInfo.status==1).order_by(schema.MaInfo.id.desc()).first()
        orm.session.commit()
        latest_id = 0
        if latest_line is not None:
            latest_id = latest_line.id
        to_fill_size = int((now - latest_id)/interval)

        #获取status=0对应的id
        latest_status0_lines = orm.session.query(schema.MaInfo).filter(schema.MaInfo.currency_type==currency_type,
                schema.MaInfo.period==duration,
                schema.MaInfo.status==0).all()
        for line in latest_status0_lines:
            zero_ids.add(line.id)

        fetch_size = to_fill_size + Slist[0] - 1 #按照最大值来获取数据
        total_price_list = self.GetPriceList(currency_type, duration, fetch_size)
        if len(total_price_list) != fetch_size:
            log_warn("enough data in table %s of currency_type=%s . get %d items while %d items is expected"%(ptable, currency_type, len(total_price_list), fetch_size));


        update_num = 0
        add_num = 0
        for step in Slist:
            price_list = total_price_list[0:to_fill_size + step -1]
            price_list = sorted(price_list, key=lambda price:price.id)

            update_num = 0
            for i in range(step-1, len(price_list)):
                array = price_list[i - step + 1 : i+1]
                close_price_list = [x.close_ for x in array]
                ma = sum(close_price_list)/step
                status = 0
                if now - tmp.id > interval:
                    status = 1
                ts = price_list[i].id
                if ts in zero_ids:
                    update_num += 1
                    orm.session.query(schema.MaInfo).filter(orm.currency_type==currency_type,
                            orm.period==duration,
                            delta==step,
                            status==0,
                            id==ts).update({"close":ma, "status":status})
                    orm.session.commit()
                else:
                    add_num += 1
                    ma_info = schema.MaInfo(id=ts,
                            close=ma,
                            period=duration,
                            currency_type=currency_type,
                            status=status,
                            delta=step,
                            price_date=timestamp2string(ts))
                    orm.session.add(ma_info)
            orm.session.commit()
            log_info("StoreMa.  update_num=%d || add_num=%d || MA=%d || currency_type=%s || duration=%s"%(update_num, add_num, step, currency_type, duration))


    #获取最近28天的多空比
    def GetLSRatio(self, contract_type, currency_type, market, ts_end = 0, period=var.Day):
        if ts_end == 0:
            ts_end = int(time.time())
        ts_begin = ts_end - 3600 * hours
        latestLsRatioLines = orm.session.query(schema.LongShortRatio).filter(schema.LongShortRatio.market==market,
                schema.LongShortRatio.contract_type==contract_type,
                schema.LongShortRatio.currency_type==currency_type,
                schema.LongShortRatio.id<=ts_end,
                schema.LongShortRatio.id>=ts_begin,
                schema.LongShortRatio.id%1800==0).order_by(schema.LongShortRatio.id.desc()).all()
        orm.session.commit()
        return latestLsRatioLines

    def StoreLongShortRatio(self, currency_type, period=Hour):
        log_info("going to store long short ratio. currency_type=%s || period=%s"%(currency_type, period))
        align_seconds = var.Duration2second[period]
        if align_seconds > 3600*4:
            align_seconds = 3600*4 #日K级别数据，考虑到时差问题
        one_week_ago = int(time.time()) - 7 * 24 * 3600
        market = 'Huobi'
        for contract_type in var.ContractTypes:
            base_lsr = schema.LongShortRatio()
            base_lsr.market = 'Huobi'
            base_lsr.currency_type = currency_type

            db_lines_to_store = {}
            base_lsr.contract_type = contract_type

           #获取db最近的7Day条记录, 避免重复插入
            latestLsRatioLines = orm.session.query(schema.LongShortRatio).filter(schema.LongShortRatio.market=='Huobi',
                    schema.LongShortRatio.contract_type==contract_type,
                    schema.LongShortRatio.currency_type==currency_type,
                    # schema.LongShortRatio.id>=one_week_ago,
                    schema.LongShortRatio.id%align_seconds==0).order_by(schema.LongShortRatio.id.desc()).limit(300).all()
            orm.session.commit()

            contains = set()
            for each in latestLsRatioLines:
                contains.add(int(each.id))
            log_info("exists key for contract_type=%s, market=%s, currency_type=%s, period=%s. [%s]"%(contract_type, market, currency_type, period, contains))

            #获取多空比数据，注意：多空比数据中的时间序列可能不等
            #提取多空比中公共的时间序列数据，实现同一时间序列的原子插入
            for ls_type in var.LsTypes:
                buySellList = GetLongShortRatio(contract_type, ls_type, currency_type, period)

                for bsInfo in buySellList:
                    base_lsr.id = bsInfo.id_
                    if bsInfo.id_ in contains:
                        #已经存在于db中
                        continue
                    if int(bsInfo.id_) % align_seconds != 0:
                        #时间序列未align
                        log_error("duration is not align to %d, with id: %d(%s)", align_seconds, bsInfo.id_, timestamp2string(bsInfo.id_))
                        continue

                    if bsInfo.id_ not in db_lines_to_store:
                        #新的序列
                        base_lsr.price_date = timestamp2string(bsInfo.id_)
                        newLsr = schema.LongShortRatio()
                        newLsr = copy.deepcopy(base_lsr)
                        db_lines_to_store[bsInfo.id_] = newLsr
                        newLsr.amount_buy_ratio = -1.0
                        newLsr.amount_sell_ratio = -1.0
                        newLsr.account_buy_ratio = -1.0
                        newLsr.account_sell_ratio = -1.0
                    tmpBsInfo = db_lines_to_store[bsInfo.id_]
                    if ls_type == "amount":
                        tmpBsInfo.amount_buy_ratio = bsInfo.buy_ratio_
                        tmpBsInfo.amount_sell_ratio = bsInfo.sell_ratio_
                    elif ls_type == "account":
                        tmpBsInfo.account_buy_ratio = bsInfo.buy_ratio_
                        tmpBsInfo.account_sell_ratio = bsInfo.sell_ratio_

            #同时存储账户多空比+持仓多空比
            for bsInfoLine in db_lines_to_store.values():
                if bsInfoLine.amount_buy_ratio <= 0 or bsInfoLine.account_buy_ratio <= 0:
                    #数据完整性验证
                    continue
                session.add(bsInfoLine)
            session.commit()

    def StorePrice(self, currency_type, period, size=100):
        interval = Duration2second[period]
        #获取最新status=1
        latest_valid_line = orm.session.query(schema.PriceInfo).filter(schema.PriceInfo.period==period,
                schema.PriceInfo.currency_type==currency_type,
                schema.PriceInfo.status==1).order_by(schema.PriceInfo.id.desc()).first()
        orm.session.commit()
        latest_id = 0
        if latest_valid_line is not None:
            latest_id = latest_valid_line.id
        
        #获取当前status=0的记录
        zero_status_record = orm.session.query(schema.PriceInfo).filter(schema.PriceInfo.period==period,
                schema.PriceInfo.currency_type==currency_type,
                schema.PriceInfo.status==0).order_by(schema.PriceInfo.id.desc()).all()
        orm.session.commit()
        zero_status_set={0}
        for line in zero_status_record:
            zero_status_set.add(line.id)


        now = time.time()
        size = int(1.0*(now- latest_id)/interval)
        missed_number = min(size, 100)
        log_info("UpdatePrice begin: to_update_num=%d || currency_type=%s || period=%s " % (missed_number, currency_type, period))

        price_list = GetCurrentKline(currency_type, period, missed_number)
        get_num = len(price_list)
        rec_num = get_num
        #按照时间的从小到大进行插入
        price_list = sorted(price_list, key=lambda price:price.id_)
        add_num = 0
        update_num = 0
        for i in range(0,len(price_list)):
            kl = price_list[i]
            ts = kl.id_
            if i%100 == 0:
                log_info("update price data for currency_type=%s || duration=%s || ts=%s"%(currency_type, period, timestamp2string(ts)))
            this_status= 0
            if now - ts > interval:
                this_status = 1
            price_info = schema.PriceInfo(id = ts,
                    period = period,
                    status = this_status,
                    currency_type = currency_type,
                    open = kl.open_,
                    high = kl.high_,
                    low = kl.low_,
                    close = kl.close_,
                    volume = kl.amount_,
                    price_date = timestamp2string(ts))
            if ts in zero_status_set:
                #status=0的记录需要更新
                update_num = update_num + 1
                orm.session.query(schema.PriceInfo).filter(schema.PriceInfo.currency_type==currency_type,
                        schema.PriceInfo.status==0,
                        schema.PriceInfo.period==period).update({"status":this_status, "high":kl.high_, "low":kl.low_, "close":kl.close_, "volume":kl.amount_})
                orm.session.commit()
            else:
                add_num = add_num + 1
                orm.session.add(price_info)
        orm.session.commit()
        log_info("UpdatePrice end: add_num=%d || update_num=%d || currency_type=%s || period=%s " % (add_num, update_num, currency_type, period))


        return
    def Migration():
        #get
        #latestline = orm.session.query(schema.Dail)..all()
        #insert
        pass
        #insert
