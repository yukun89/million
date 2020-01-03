#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : store.py
# Date              : 02.06.2019
# Last Modified Date: 02.06.2019
#read and write info from/to mysql
from hlog import *
from ds import *
from fetch import *
import pymysql
import time
import datetime
import cmath
from decimal import Decimal

def timestamp2dstring(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d")
        return str1
    except Exception as e:
        print(e)
    return ''

def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return str1
    except Exception as e:
        print(e)
    return ''

#update data in table
class MysqlSafeCursor:
    def __init__(self,conn = None,retry=2):
        if conn == None:
            self.__conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='Root@Mysql123.',db='huobi',charset='utf8')
            self.__need_close_conn = True
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


def GetBollList(currency_type, fetch_size, now_id = 0):
    ctype = currency_type
    if now_id == 0:
        UpdateMa(currency_type, duration)
    cursor = MysqlSafeCursor()
    ktable = Duration2ktable[duration]
    dsecond = Duration2second[duration]
    if now_id <= 0 :
        select_sql = "select id, close from %s where currency_type='%s' and delta=%d order by price_date desc limit %d" % (ktable, currency_type, step, fetch_size)
    else :
        select_sql = "select id, close from %s where currency_type='%s' and delta=%d and id <= %d order by price_date desc limit %d" % (ktable, currency_type, step, now_id, fetch_size)
        
    cursor.execute(select_sql)
    lines = cursor.fetchall()
    price_list = []
    if lines == None:
        return
    latest_id_in_price = int(lines[0][0])
    #get the data for calculate MA, lean of data = to_fill_size + step -1
    tmp = latest_id_in_price
    for i in range(len(lines)):
        price = Price(currency_type)
        line = lines[i]
        price.id_ = line[0]
        if i >=1  and tmp - price.id_  != dsecond:
            log_error("some data is lost in table %s || ctype %s || id %d || last_one %d)"%(ktable, ctype, price.id_, tmp))
            exit(-1)
        price.close_ = line[1]
        price_list.append(price)
        tmp = price.id_
    return price_list


def GetMAList(currency_type, duration, step, fetch_size, now_id = 0):
    ctype = currency_type
    if now_id == 0:
        UpdateMa(currency_type, duration, step)
    cursor = MysqlSafeCursor()
    ktable = Duration2ktable[duration]
    dsecond = Duration2second[duration]
    if now_id <= 0 :
        select_sql = "select id, close from %s where currency_type='%s' and delta=%d order by price_date desc limit %d" % (ktable, currency_type, step, fetch_size)
    else :
        select_sql = "select id, close from %s where currency_type='%s' and delta=%d and id <= %d order by price_date desc limit %d" % (ktable, currency_type, step, now_id, fetch_size)
        
    cursor.execute(select_sql)
    lines = cursor.fetchall()
    price_list = []
    if lines == None:
        return
    latest_id_in_price = int(lines[0][0])
    #get the data for calculate MA, lean of data = to_fill_size + step -1
    tmp = latest_id_in_price
    for i in range(len(lines)):
        price = Price(currency_type)
        line = lines[i]
        price.id_ = line[0]
        if i >=1  and tmp - price.id_  != dsecond:
            log_error("some data is lost in table %s || ctype %s || id %d || last_one %d)"%(ktable, ctype, price.id_, tmp))
            exit(-1)
        price.close_ = line[1]
        price_list.append(price)
        tmp = price.id_
    return price_list
    pass

def GetPriceList(currency_type, duration, fetch_size, now_id = 0):
    ctype = currency_type
    if now_id == 0:
        UpdateKline(currency_type, duration)
    cursor = MysqlSafeCursor()
    ptable = Duration2ptable[duration]
    dsecond = Duration2second[duration]
    if now_id <= 0 :
        select_sql = "select id, close, open, high, low from %s where currency_type='%s' order by price_date desc limit %d" % (ptable, currency_type, fetch_size)
    else :
        select_sql = "select id, close, open, high, low from %s where currency_type='%s' id <= %d order by price_date desc limit %d" % (ptable, currency_type, now_id, fetch_size)
        
    cursor.execute(select_sql)
    lines = cursor.fetchall()
    price_list = []
    if lines == None:
        return
    latest_id_in_price = int(lines[0][0])
    #get the data for calculate MA, lean of data = to_fill_size + step -1
    tmp = latest_id_in_price
    for i in range(len(lines)):
        price = Price(currency_type)
        line = lines[i]
        price.id_ = line[0]
        if i >=1  and tmp - price.id_  != dsecond:
            log_error("some data is lost in table %s || ctype %s || id %d || early id : %d)"%(ptable, ctype, tmp, price.id_))
            exit(-1)
        price.close_ = line[1]
        price.open_ = line[2]
        price.high_= line[3]
        price.low_ = line[4]
        price_list.append(price)
        tmp = price.id_
    return price_list

#note: the data can be only updated to yesterday.
def UpdateBoll(currency_type):
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
    price_list = GetPriceList(currency_type, duration, fetch_size)
    if len(price_list) != fetch_size:
        log_warn("no enough data in table %s of ctype %s @ step %d. get %d items while %d items is expected"%(ptable, ctype, step, len(price_list), fetch_size));
    cursor = MysqlSafeCursor()
    for i in range(to_fill_size):
        length = step
        if i + length >= len(price_list):
            length = len(price_list) - i
        if length == 0 :
            break
        array = price_list[i:i+length]
        close_price_list = [x.close_ for x in array]
        price_list[i].avg_ = sum(close_price_list)/length
        avg = price_list[i].avg_
        variance = sum([(avg - x)*(avg - x) for x in close_price_list])/length
        std_variance = variance ** (Decimal(0.5))
        upper = avg + 2 * std_variance
        lower = avg - 2 * std_variance
        tmp = price_list[i]
        sql = "insert into boll values (%d, \'%s\', \'%s\', %f, %f, %f) on duplicate key update id=%d,currency_type=\'%s\',price_date=\'%s\',mid=%f,upper=%f,lower=%f"%(tmp.id_, ctype, timestamp2string(tmp.id_), avg, upper, lower, tmp.id_, ctype, timestamp2string(tmp.id_), avg, upper, lower)
        cursor.execute(sql)
        if cursor.execute(sql) == False:
            log_error("Failed to execute %s"%sql)
    pass

def UpdateMa(currency_type, duration, step = 5):
    ctype = currency_type
    ktable = Duration2ktable[duration]
    ptable = Duration2ptable[duration]
    tid, to_fill_size = getLatestIdOfPrice(currency_type, duration, ktable)
    if to_fill_size < 1:
        log_info("MA%d of %s@%s is up to date"%(step, currency_type, duration))
        return 0
    fetch_size = to_fill_size + step -1
    price_list = GetPriceList(currency_type, duration, fetch_size)
    if len(price_list) != fetch_size:
        log_warn("no enough data in table %s of ctype %s @ step %d. get %d items while %d items is expected"%(ptable, ctype, step, len(price_list), fetch_size));
    cursor = MysqlSafeCursor()
    for i in range(to_fill_size):
        length = step
        if i + length >= len(price_list):
            length = len(price_list) - i
        if length == 0 :
            break
        array = price_list[i:i+length]
        close_price_list = [x.close_ for x in array]
        price_list[i].avg_ = sum(close_price_list)/length
        tmp = price_list[i]
        #id, currency_type, close, price_date
        sql="insert into %s values (%d,\'%s\',%f, %d, \'%s\') on duplicate key update id=%d,currency_type=\'%s\',close=%f,delta=%d,price_date=\'%s\'"%\
            (ktable, tmp.id_, currency_type, tmp.close_, step, timestamp2string(tmp.id_)
             ,tmp.id_, currency_type, tmp.close_, step, timestamp2string(tmp.id_))
        if cursor.execute(sql) == False:
            log_error("Failed to execute %s"%sql)
    log_info("Succeed Update %d items about MA%d for %s@%s"%(to_fill_size, step, currency_type, duration))
    return 0

#从某个表格中获取最新数据，返回最新id和需要更新的数量.
#注意我们返回的是完整数据的最新id。例如数据为1， 2， 3，4， 6， 7， 8. 那么我们返回的值是4
def getLatestIdOfPrice(currency_type, duration, table):
    now  = int(time.time())
    missed_number = 2000
    one_month_early = now - 3600 * 24 * 30
    cursor = MysqlSafeCursor()
    cursor.execute("select id from %s where currency_type='%s' and id > %d order by id asc limit 2000" % (table, currency_type, one_month_early))
    fields = cursor.fetchall()
    if fields == None :
        return 0, missed_number
    latest_record_date_id = fields[0][0]#第一行第一列
    for line in fields:
        currend_id = line[0]
        if currend_id - latest_record_date_id > Duration2second[duration] :
            break
        else:
            latest_record_date_id = currend_id
    size = int(1.0*(now- latest_record_date_id)/Duration2second[duration])
    missed_number = min(size,2000)
    log_info("now is %d, while the latest id is %d for currency %s in table %s. %d items missing)"%(now, latest_record_date_id, currency_type, table, missed_number))
    return latest_record_date_id, missed_number

def UpdateDailyKline(currency_type):
    UpdateKline(currency_type, Day)
    return

#更新mysql中存储的K线指标
def UpdateKline(currency_type, duration, refresh = False):
    """
    :param period: "1min"  "5min"  "15min"  "30min"  "60min"   "4hour" "1day"
    :param currency_type: "htusdt" ...
    """
    table = Duration2ptable[duration]
    tid, size = getLatestIdOfPrice(currency_type, duration, table)
    if size < 1:
        log_info("price of %s is up to date", currency_type)
        if refresh:
            size = 1
        else:
            return 0
    log_info("tid is %d, record need request size:%d currency_type:%s period:%s" % (tid, size, currency_type, duration))
    price_list = GetCurrentKline(currency_type, duration, size)
    get_num = len(price_list)
    rec_num = get_num
    now  = int(time.time())
    for i in range(0,len(price_list)):
        kl = price_list[i]
        #if kl.id_ > now - Duration2second[duration]:
            #log_error("skip update id %d for %s@%s for the data is broken"%(kl.id_, currency_type, table))
            #rec_num -= 1
            #continue
        log_info("update data for %s on %s"%(currency_type, timestamp2string(kl.id_)))
        sql="insert into %s values (%d,\'%s\',%f,%f,%f,%f,%f,\'%s\') on duplicate key update id=%d,currency_type=\'%s\',open=%f,high=%f,low=%f,close=%f,amount=%f,price_date=\'%s\'"%\
            (table, kl.id_, currency_type, kl.open_, kl.high_, kl.low_, kl.close_, kl.amount_, timestamp2string(kl.id_)
             ,kl.id_, currency_type, kl.open_, kl.high_, kl.low_, kl.close_, kl.amount_, timestamp2string(kl.id_))
        cursor = MysqlSafeCursor()
        if cursor.execute(sql) == False:
            log_error("Failed to execute sql %s"%(sql))
            rec_num -= 1
    log_info("record kline succ_num:%d currency_type:%s period:%s total_get_num:%d" % (rec_num, currency_type, duration, get_num))
    if get_num != rec_num:
        return -1
    else:
        return 0
