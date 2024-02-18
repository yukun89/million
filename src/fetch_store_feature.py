import time
import orm
from api import etc
from ok_api import public_wrapper
from util import common

def timestamp2datetime(timestamp):
    time_array = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def timestamp2date(timestamp):
    time_array = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d", time_array)


def update_greedy_fear_index(is_batch=False):
    if not is_batch:
        raw_data = etc.get_greedy_fear_index_now()
        daily_greedy_fear_index = orm.Schema.DailyGreedyFearIndex(ts=raw_data["timestamp"],
                                                                  mtime=timestamp2datetime(int(raw_data["timestamp"])),
                                                                  greedy_fear_index=raw_data["value"])
        orm.session.add(daily_greedy_fear_index)
        orm.session.commit()
    else:
        greedy_fear_index_multi_lines = etc.get_greedy_fear_index_history()
        for line in greedy_fear_index_multi_lines:
            print("update line: %s" % line)
            daily_greedy_fear_index = orm.Schema.DailyGreedyFearIndex(ts=line["timestamp"],
                                                                      mtime=timestamp2datetime(int(line["timestamp"])),
                                                                      greedy_fear_index=line["value"])
            orm.session.merge(daily_greedy_fear_index)
        orm.session.commit()
    return



def update_kline_data_all(instId, bar):
    #获取从2018年以后的所有数据
    if bar not in common.bar_list:
        print("Invalid bar:%s" % bar)
        return
    current_time = int(time.time())
    start_ts = common.start_ts + 86400*365*1
    batch_num = 100
    step = common.bar_sec_dict[bar] * batch_num
    for cur in range(start_ts, current_time, step):
        before = cur
        after = cur + step
        resp = public_wrapper.marketDataAPI.get_history_candlesticks(instId=instId, bar=bar, before=before)
        if resp['code'] != '0':
            print("Error: failed to get k line. instId = %s || bar = %s || before = %s || after = %s" % (instId, bar, before, after))
            continue
        data = resp['data']
        if len(data) == 0:
            print("Empty data: k line. instId = %s || bar = %s || before = %s || after = %s || start = %s" % (instId, bar, before, after, timestamp2datetime(before)))
            continue
        for line in data:
            ts = int(int(line[0]) / 1000)
            o = float(line[1])
            h = float(line[2])
            l = float(line[3])
            c = float(line[4])
            vol = line[5]
            volCcy = line[6]
            volCcyQuote	= line[7]
            confirm = line[8]
            kline = orm.Schema.Kline(ts=ts,
                                     mtime=timestamp2datetime(ts),
                                     symbol=instId,
                                     duration = "min",
                                     o_price=o,
                                     h_price=h,
                                     l_price=l,
                                     c_price=c)
            orm.session.merge(kline)
        orm.session.commit()
    return


if __name__ == "__main__":
    #update_greedy_fear_index(is_batch=False)
    update_kline_data_all("BTC-USDT", "1H")
