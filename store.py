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
import copy
import var

#update data in table
class MysqlSafeCursor:
    def __init__(self,conn = None,retry=2):
        if conn == None:
            for index in range(retry):
                try:
                    self.__conn = pymysql.Connect(host='127.0.0.1',port=3306,user='ykhuang',passwd='m159357M.',db='huobi',charset='utf8')
                    self.__need_close_conn = True
                except Exception as e:
                    log_warn("Failed to create mysql connection for %s"%(e))
        else:
            self.__conn = conn
            self.__need_close_conn = False
        self.__cursor = self.__conn.cursor()
        self.__retry = retry

    def __del__(self):
        try:
            self.__cursor.close()
            if self.__need_close_conn:
                self.__conn.close()
        except:
            log_error("Del MysqlSafeCursor error")
    def execute(self,sql):
        for i in range(0,self.__retry):
            try:
                self.__cursor.execute(sql)
                self.__conn.commit()
                return  True
            except:
                try:
                    self.__conn.connect()
                    self.__cursor = self.__conn.cursor()
                except:
                    log_error("[SQL ERROR] %s"%(sql))
        return False
    def fetchone(self):
        try:
            return self.__cursor.fetchone()
        except:
            return None
    def fetchall(self):
        try:
            return self.__cursor.fetchall()
        except:
            return None

class QueryResp:
    def __init__(self):
        self.ok_=False
        self.data_=[]
        pass

def Query(fields, table, condition, display=""):
    resp=QueryResp()
    columns = ','.join(fields)
    sql = "select %s from %s where %s %s"%(columns, table, condition, display)

    cursor = MysqlSafeCursor()
    if cursor.execute(sql) == False:
        log_error("Failed to query with [%s]"%sql)
        return
    lines = cursor.fetchall()

    if lines == None:
        return resp
    resp.ok_ = True
    for line in lines:
        line_data={}
        index = 0
        for field in fields:
            line_data[field] = line[index]
            index += 1
        resp.data_.append(line_data)

    return resp

#从某个表格中获取最新数据，返回最新id和需要更新的数量.
#注意我们返回的是完整数据的最新id。例如数据为1， 2， 3，4，<5>,  6， 7， 8. 那么我们返回的值是4(缺失的是5)
def getLatestIdOfPrice(currency_type, duration, table, delta = 0, only_active=True):
    log_info("request_in. getLatestIdOfPrice: going to get latest id of price ct=%s, duration=%s" %(currency_type, duration))
    now  = int(time.time())
    missed_number = 2000 #API只能返回这么多
    duration_in_sec = Duration2second[duration]
    longest_recall_duration = missed_number * duration_in_sec
    since_from_id = now - longest_recall_duration
    #从since_from_id 到目前位置，缺失的最早的id
    cursor = MysqlSafeCursor()
    query_latest_id_sql = ""
    status_threshold = -1
    if only_active:
        status_threshold = 0
    if delta == 0 :
        query_latest_id_sql = "select id from %s where currency_type='%s' and id > %d  and status > %d order by id asc limit 100000" % (table, currency_type, since_from_id, status_threshold)
    else:
        query_latest_id_sql = "select id from %s where currency_type='%s' and id > %d and delta = %d and status > %d order by id asc limit 100000" % (table, currency_type, since_from_id, delta, status_threshold)
    cursor.execute(query_latest_id_sql)
    fields = cursor.fetchall()
    if fields == None :
        return 0, missed_number
    if len(fields) == 0 or len(fields[0]) == 0:
        log_warn("Lost data for more than half a year. so empty query: %s" % (query_latest_id_sql))
        latest_record_date_id = 0
    else:
        latest_record_date_id = fields[0][0]#第一行第一列
    for line in fields:
        currend_id = line[0]
        if currend_id - latest_record_date_id > Duration2second[duration] :
            break
        else:
            latest_record_date_id = currend_id
    size = int(1.0*(now- latest_record_date_id)/Duration2second[duration])
    missed_number = min(size, 2000)
    log_info("request_out. getLatestIdOfPrice. now=%d || latest id=%d || currency=%s || table=%s. missed_number=%d || duration=%s"%(now, latest_record_date_id, currency_type, table, missed_number, duration))
    return latest_record_date_id, missed_number


#对mysql中的业务数据进行读写:主要是Get/Store方法
class MysqlStore:
    def __init__(self):
        pass

    #从数据库中获取boll指标
    def GetBollList(self, currency_type, duration=Day, fetch_size=20, now_id = 0):
        ctype = currency_type
        cursor = MysqlSafeCursor()
        ktable = "boll"
        dsecond = 24 * 3600
        if now_id <= 0 :
            select_sql = "select id, mid, upper, lower from %s where currency_type='%s' and duration = '%s' order by price_date desc limit %d" % (ktable, currency_type, duration, fetch_size)
        else :
            select_sql = "select id, mid, upper, lower from %s where currency_type='%s' and id <= %d and duration = '%s' order by price_date desc limit %d" % (ktable, currency_type, now_id, duration, fetch_size)
        cursor.execute(select_sql)
        lines = cursor.fetchall()
        price_list = []
        if lines == None or len(lines) == 0 or len(lines[0]) == 0:
            return price_list
        latest_id_in_price = int(lines[0][0])
        tmp = latest_id_in_price
        for i in range(len(lines)):
            price = Price(currency_type)
            line = lines[i]
            price.id_ = line[0]
            if i >=1  and tmp - price.id_  != dsecond:
                log_error("some data is lost in table %s || ctype %s || id %d || last_one %d)"%(ktable, ctype, price.id_, tmp))
                exit(-1)
            price.boll_mid_ = float(line[1])
            price.boll_high_ = float(line[2])
            price.boll_low_ = float(line[3])
            price_list.append(price)
            tmp = price.id_
        return price_list

    #从数据库中获取MA指标
    def GetMAList(self, currency_type, duration, fetch_size, now_id = 0):
        ctype = currency_type
        cursor = MysqlSafeCursor()
        ktable = Duration2ktable[duration]
        dsecond = Duration2second[duration]
        if now_id <= 0 :
            select_sql = "select id, delta, close from %s where currency_type='%s' order by id desc, delta desc limit %d" % (ktable, currency_type, fetch_size * 7)
        else :
            select_sql = "select id, delta, close from %s where currency_type='%s' and id <= %d order by id desc, delta desc limit %d" % (ktable, currency_type, now_id, fetch_size * 7)
        cursor.execute(select_sql)
        lines = cursor.fetchall()
        price_list = []
        if lines == None or len(lines) == 0 or len(lines[0]) == 0 :
            return price_list
        latest_id_in_price = int(lines[0][0])
        #get the data for calculate MA, lean of data = to_fill_size + step -1
        tmp = latest_id_in_price
        price = Price(currency_type)
        price.id_ = tmp
        price_list.append(price)
        for i in range(len(lines)):
            line = lines[i]
            tid = line[0]
            #price.id_ = line[0]
            if i >=1  and ( tid + dsecond != tmp and tid != tmp):
                log_error("some data is lost in table %s || ctype %s || id %d || last_one %d || real duration %d || expected_duration: %d)"%(ktable, ctype, tid, tmp, tmp - tid, dsecond))
                exit(-1)
            price = price_list[len(price_list) - 1]
            if tid != price.id_:
                price = Price(currency_type)
                price.id_ = tid
                price_list.append(price)
            tdelta = int(line[1])
            tclose = float(line[2])
            if tdelta == 5:
                price.ma5_ = tclose
                pass
            elif tdelta == 10:
                price.ma10_ = tclose
                pass
            elif tdelta == 20:
                price.ma20_ = tclose
                pass
            elif tdelta == 30:
                price.ma30_ = tclose
                pass
            elif tdelta == 60:
                price.ma60_ = tclose
                pass
            elif tdelta == 90:
                price.ma90_ = tclose
                pass
            elif tdelta == 120:
                price.ma120_ = tclose
                pass
            tmp = tid
        return price_list

    #降序排列: 获取now_id 之前的数据
    def GetPriceList(self, currency_type, duration, fetch_size, now_id = 0):
        ctype = currency_type
        cursor = MysqlSafeCursor()
        ptable = Duration2ptable[duration]
        dsecond = Duration2second[duration]
        if now_id <= 0 :
            select_sql = "select id, close, open, high, low from %s where currency_type='%s' order by price_date desc limit %d" % (ptable, currency_type, fetch_size)
        else :
            select_sql = "select id, close, open, high, low from %s where currency_type='%s' and id < %d order by price_date desc limit %d" % (ptable, currency_type, now_id+1, fetch_size)
        cursor.execute(select_sql)
        log_info("GetPriceList: sql=%s"%(select_sql))
        lines = cursor.fetchall()
        price_list = []
        if lines == None or len(lines) == 0:
            log_error(select_sql)
            return price_list
        latest_id_in_price = int(lines[0][0])
        #get the data for calculate MA, lean of data = to_fill_size + step -1
        tmp = latest_id_in_price
        for i in range(len(lines)):
            price = Price(currency_type)
            line = lines[i]
            price.id_ = line[0]
            if i >=1  and tmp - price.id_  != dsecond:
                #当前数据的差值和前一条数据时间上gap过大
                log_error("some data is lost in table %s || ctype %s || id %d || early id : %d)"%(ptable, ctype, tmp, price.id_))
                price_list.clear()
                tmp = price.id_
            price.close_ = line[1]
            price.open_ = line[2]
            price.high_= line[3]
            price.low_ = line[4]
            price_list.append(price)
            tmp = price.id_
        return price_list


    def StoreBoll(self, currency_type, duration):
        ctype = currency_type
        duration = Day
        step = 20
        btable = "boll"
        ptable = Duration2ptable[duration]
        tid, to_fill_size = getLatestIdOfPrice(currency_type, duration, btable)
        if to_fill_size < 1:
            log_info("boll for currency %s is up to date"%(currency_type))
            return 0
        fetch_size = to_fill_size + step -1
        price_list = self.GetPriceList(currency_type, duration, fetch_size)
        cursor = MysqlSafeCursor()
        price_list = sorted(price_list, key=lambda price:price.id_)
        now  = int(time.time())
        interval = Duration2second[duration]
        if len(price_list) != fetch_size:
            log_warn("UpdateBoll no enough data in table %s of ctype=%s || step=%d. get %d items while %d items is expected. from %s to %s"%(ptable, ctype, step, len(price_list), fetch_size, timestamp2string(price_list[0].id_), timestamp2string(price_list[-1].id_)));
        for i in range(step-1, len(price_list)):
            array = price_list[i+1 - step : i+1]
            close_price_list = [x.close_ for x in array]
            price_list[i].avg_ = sum(close_price_list)/step
            avg = price_list[i].avg_
            variance = sum([(avg - x)*(avg - x) for x in close_price_list])/step
            std_variance = variance ** (Decimal(0.5))
            upper = avg + 2 * std_variance
            lower = avg - 2 * std_variance
            price_list[i].boll_mid_ = avg
            price_list[i].boll_high_ = upper
            price_list[i].boll_low_ = lower
            tmp = price_list[i]
            status = 0
            if now - tmp.id_ > interval:
                status = 1
            #id, status, currency_type, duration, price_date, mid, upper, lower
            #sql = "insert into boll values (%d, %d, \'%s\', \'%s\', \'%s\',%f, %f, %f) on duplicate key update id=%d, status=%d, currency_type=\'%s\',price_date=\'%s\',duration=\'%s\',mid=%f,upper=%f,lower=%f"%(tmp.id_, status, ctype, timestamp2string(tmp.id_), duration, avg, upper, lower, tmp.id_, status, ctype, timestamp2string(tmp.id_), duration, avg, upper, lower)
            sql = "insert into boll values (%d, %d, \'%s\', \'%s\', \'%s\',%f, %f, %f) on duplicate key update status=%d, mid=%f,upper=%f,lower=%f"%(tmp.id_, status, ctype, duration, timestamp2string(tmp.id_), avg, upper, lower, status, avg, upper, lower)
            cursor.execute(sql)
            if cursor.execute(sql) == False:
                log_error("Failed to execute %s"%sql)
        return price_list

    #获取时间点之前的macd曲线
    def UpdateMacd(self, currency_type, duration):
        log_info("request_in UpdateMacd: ct=%s || duration=%s || step=%d", currency_type, duration)
        ctype = currency_type
        macd_table = "macd"
        ptable = Duration2ptable[duration]
        fast = 12
        slow = 26
        factor = 9
        #todo: refactor getLatestIdOfPrice
        #step1 获取需要更新的macd采样点数量
        tid, to_fill_size = getLatestIdOfPrice(currency_type, duration, macd_table)
        if to_fill_size < 1:
            if refresh:
                to_fill_size = 1 # 刷新最新一条MA
            else:
                log_info("macd currency_type=%s || duration=%s is up to date"%(currency_type, duration))
                return 0
        #step2: 确定需要的Price采样点个数
        fetch_size = to_fill_size + slow -1
        price_list = self.GetPriceList(currency_type, duration, fetch_size)
        if len(price_list) != fetch_size:
            log_warn("no enough data in table %s of ctype %s @ step %d. get %d items while %d items is expected"%(ptable, ctype, slow, len(price_list), fetch_size));

        cursor = MysqlSafeCursor()
        update_num = 0
        interval = Duration2second[duration]
        now  = int(time.time())
        for i in range(len(price_list)):
            length = slow #实际长度==
            if i + length >= len(price_list):
                length = len(price_list) - i
            if length != step :
                log_warn("UpdateMacd: data not enough, skip is ok. data_length=%d || Ma%d || currency_type=%s || tid=%s."%(length, step, ctype, price_list[i].id_))
                break
            array = price_list[i:i+length]
            close_price_list = [x.close_ for x in array]
            dma12 = (sum(close_price_list)+price_list[i].close_)/(length+1)
            tmp = Price(currency_type)
            tmp.id_ = price_list[i].id_
            tmp.close_ = ma
            if now - tmp.id_ > interval:
                status = 1
            else:
                status = 0
            #id, currency_type, close, price_date
            sql="insert into %s values (%d,%d,\'%s\',%f, %d, \'%s\') on duplicate key update id=%d,status=%d,currency_type=\'%s\',close=%f,delta=%d,price_date=\'%s\'"%\
                (ktable, tmp.id_, status, currency_type, tmp.close_, step, timestamp2string(tmp.id_)
                 ,tmp.id_, status, currency_type, tmp.close_, step, timestamp2string(tmp.id_))
            if cursor.execute(sql) == False:
                log_error("Failed to execute %s"%sql)
            else:
                update_num += 1

        log_info("request_out. UpdateMacd.  update_num=%d || MA=%d || currency_type=%s || duration=%s"%(update_num, step, currency_type, duration))

        pass


    #以当前需要更新的索引为1，如果需要更新10个M5均线，那么需要获取14条数据（最后一条数据是需要用10-11-12-13-14来更新）
    def StoreMa(self, currency_type, duration, refresh = True):
        log_info("request_in StoreMa: ct=%s || duration=%s ", currency_type, duration)
        now  = int(time.time())
        interval = Duration2second[duration]

        #Step的list
        Slist = (5, 10, 20, 30, 60)
        ctype = currency_type
        ktable = Duration2ktable[duration]
        ptable = Duration2ptable[duration]

        tid, to_fill_size = getLatestIdOfPrice(currency_type, duration, ktable)
        if to_fill_size < 1:
            if refresh:
                to_fill_size = 1 # 刷新最新一条MA
            else:
                log_info("MA of %s@%s is up to date"%(currency_type, duration))
                return 0

        fetch_size = to_fill_size + Slist[-1] - 1 #按照最大值来获取数据
        total_price_list = self.GetPriceList(currency_type, duration, fetch_size)
        if len(total_price_list) != fetch_size:
            log_warn("enough data in table %s of ctype %s . get %d items while %d items is expected"%(ptable, ctype, len(total_price_list), fetch_size));

        cursor = MysqlSafeCursor()

        for step in Slist:
            price_list = total_price_list[0:to_fill_size + step -1]
            price_list = sorted(price_list, key=lambda price:price.id_)

            update_num = 0
            for i in range(step-1, len(price_list)):
                array = price_list[i - step + 1 : i+1]
                close_price_list = [x.close_ for x in array]
                ma = sum(close_price_list)/step
                tmp = Price(currency_type)
                tmp.id_ = price_list[i].id_
                tmp.close_ = ma
                if now - tmp.id_ > interval:
                    status = 1
                else:
                    status = 0
                #id, currency_type, close, price_date
                sql="insert into %s values (%d,%d,\'%s\',%f, %d, \'%s\') on duplicate key update id=%d,status=%d,currency_type=\'%s\',close=%f,delta=%d,price_date=\'%s\'"%\
                    (ktable, tmp.id_, status, currency_type, tmp.close_, step, timestamp2string(tmp.id_)
                     ,tmp.id_, status, currency_type, tmp.close_, step, timestamp2string(tmp.id_))
                if cursor.execute(sql) == False:
                    log_error("Failed to execute %s"%sql)
                else:
                    update_num += 1
            log_info("StoreMa.  update_num=%d || MA=%d || currency_type=%s || duration=%s"%(update_num, step, currency_type, duration))

        return 0

    #获取最近10天的多空比
    def GetLSRatio(self, contract_type, currency_type, market, ts_end = 0, period=var.Day):
        if ts_end == 0:
            ts_end = int(time.time())
        ts_begin = ts_end - 3600 * 24 * 10
        latestLsRatioLines = orm.session.query(schema.LongShortRatio).filter(schema.LongShortRatio.market==market,
                schema.LongShortRatio.contract_type==contract_type,
                schema.LongShortRatio.currency_type==currency_type,
                schema.LongShortRatio.id<=ts_end,
                schema.LongShortRatio.id>=ts_begin).order_by(schema.LongShortRatio.id.desc()).all()
        orm.session.commit()
        return latestLsRatioLines

    def get_ts_set(bsList):
        res = set([bsInfo.id_ for bsInfo in bsList])
        return res

    def StoreLongShortRatio(self, currency_type, period=var.FMin):
        log_info("going to store  long short ratio. currency_type=%s|| period=%s"%(currency_type, period))
        align_seconds = var.Duration2second[period]

        market = 'Huobi'
        for contract_type in var.ContractTypes:
            base_lsr = schema.LongShortRatio()
            base_lsr.market = 'Huobi'
            base_lsr.currency_type = currency_type

            db_lines_to_store = {}
            base_lsr.contract_type = contract_type

            #获取最近的三十条记录
            latestLsRatioLines = orm.session.query(schema.LongShortRatio).filter(schema.LongShortRatio.market=='Huobi',
                    schema.LongShortRatio.contract_type==contract_type,
                    schema.LongShortRatio.currency_type==currency_type,
                    schema.LongShortRatio.id%align_seconds==0).order_by(schema.LongShortRatio.id.desc()).limit(100).all()
            orm.session.commit()
            contains = set()
            for each in latestLsRatioLines:
                contains.add(int(each.id))
            log_info("exists key for period=%s, contract_type=%s, market=%s, currency_type=%s. [%s]"%(period, contract_type, market, currency_type, contains))

            #获取多空比数据，注意：多空比数据中的时间序列可能不等
            #提取多空比中公共的时间序列数据，实现同一时间序列的原子插入
            for ls_type in var.LsTypes:
                buySellList = GetLongShortRatio(contract_type, ls_type, currency_type, period=period)

                for bsInfo in buySellList:
                    base_lsr.id = bsInfo.id_
                    if bsInfo.id_ in contains:
                        #已经存在于db中
                        continue
                    if bsInfo.id_ % align_seconds != 0:
                        #时间序列未align
                        log_error("duration is not align to %d, with info: %s", align_seconds, bsInfo)
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
                orm.session.add(bsInfoLine)
            orm.session.commit()

    def StorePrice(self, currency_type, duration, refresh = False):
        """
        :param period: "1min"  "5min"  "15min"  "30min"  "60min"   "4hour" "1day"
        :param currency_type: "htusdt" ...
        :param refresh: "whether refresh the latest one." ...
        """
        table = Duration2ptable[duration]
        tid, size = getLatestIdOfPrice(currency_type, duration, table)
        if size < 1:
            log_info("price of %s-%s is up to date", currency_type, duration)
            if refresh:
                size = 1
            else:
                return 0
        log_info("StorePrice tid=%d || http_request_size=%d || currency_type=%s || period=%s" % (tid, size, currency_type, duration))
        price_list = GetCurrentKline(currency_type, duration, size)
        get_num = len(price_list)
        rec_num = get_num
        now  = int(time.time())
        interval = Duration2second[duration]
        #按照时间的从小到大进行插入
        price_list = sorted(price_list, key=lambda price:price.id_)
        cursor = MysqlSafeCursor()
        for i in range(0,len(price_list)):
            kl = price_list[i]
            #if kl.id_ > now - Duration2second[duration]:
                #log_error("skip update id %d for %s@%s for the data is broken"%(kl.id_, currency_type, table))
                #rec_num -= 1
                #continue
            if i%100 == 0:
                log_info("update price data for currency_type=%s || duration=%s || ts=%s"%(currency_type, duration, timestamp2string(kl.id_)))
            if now - kl.id_ > interval:
                status = 1
            else:
                status = 0
            sql="insert into %s values (%d,%d,\'%s\',%f,%f,%f,%f,%f,\'%s\') on duplicate key update id=%d,status=%d,currency_type=\'%s\',open=%f,high=%f,low=%f,close=%f,amount=%f,price_date=\'%s\'"%\
                (table, kl.id_, status, currency_type, kl.open_, kl.high_, kl.low_, kl.close_, kl.amount_, timestamp2string(kl.id_)
                 ,kl.id_, status, currency_type, kl.open_, kl.high_, kl.low_, kl.close_, kl.amount_, timestamp2string(kl.id_))
            if cursor.execute(sql) == False:
                log_error("Failed to execute sql %s"%(sql))
                rec_num -= 1
        log_info("UpdatePrice succ_num=%d || currency_type=%s || duration=%s || total_get_num=%d" % (rec_num, currency_type, duration, get_num))
        if get_num != rec_num:
            return -1
        else:
            return 0
