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
    start_ts = common.start_ts
    batch_num = 100
    step = common.bar_sec_dict[bar] * batch_num
    for cur in range(start_ts, current_time, step):
        resp = public_wrapper.marketDataAPI.get_history_candlesticks(instId=instId, bar=bar, after=cur, before=cur+step)
        print(resp['data'])
        break
    return


if __name__ == "__main__":
    update_greedy_fear_index(True)
    update_kline_data_all("BTCUSDT", "1H")
