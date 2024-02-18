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


"""
    coin_list = etc.get_coin_list()
    id_symbol_dict = {}
    for coin in coin_list:
        symbol_id = coin["id"]
        if symbol_id == "cassie-dragon":
            print("skip coin: %s" % coin)
            continue
        print("update coin: %s" % coin)
        symbol = coin["symbol"]
        name = coin["name"]
        coin_line = orm.Schema.CoinList(id=symbol_id, name=name, symbol=symbol)
        orm.session.merge(coin_line)

        id_symbol_dict[symbol_id] = symbol

    orm.session.commit()
"""


def update_coin_info():
    max_supply_updated_hour_ts = int(time.time() / 3600) * 3600
    index = 1
    while True:
        coin_list = etc.get_market_data(per_page=100, page_num=index)
        index += 1
        if coin_list is None:
            print("skip None data for index=%s"%index)
            if index < 100:
                continue
            break
        for coin in coin_list:
            print(coin)
            total_supply = 0
            if coin["total_supply"] is not None:
                total_supply = int(coin["total_supply"])

            max_supply = 0
            if coin["max_supply"] is not None:
                max_supply = int(coin["max_supply"])
            symbol = coin["symbol"]
            symbol_id = coin["id"]
            if max_supply == 0:
                print("not store 0 data for %s"%symbol)
            coin_line = orm.Schema.CoinMarket(id=symbol_id,
                                              symbol=symbol,
                                              total_supply=total_supply,
                                              max_supply=max_supply,
                                              max_supply_updated_hour_ts=max_supply_updated_hour_ts)
            # no dup data: TODO
            orm.session.merge(coin_line)
        orm.session.commit()
        if len(coin_list) < 100:
            break
    return


def update_kline_data_all(instId, bar, from_ts=0, to_ts=0):
    # 获取从2018年以后的所有数据
    if bar not in common.bar_list:
        print("Invalid bar:%s" % bar)
        return
    cur = int(time.time())
    if to_ts > 0:
        cur = to_ts

    start_ts = common.start_ts
    if from_ts > 0:
        start_ts = from_ts

    batch_num = 96
    step = common.bar_sec_dict[bar] * batch_num
    while cur >= start_ts:
        before = cur - step
        after = cur
        resp = public_wrapper.marketDataAPI.get_history_candlesticks(instId=instId,
                                                                     bar=bar,
                                                                     before=before * 1000,
                                                                     after=after * 1000,
                                                                     limit=batch_num + 1)
        if resp['code'] != '0':
            print("Error: failed to get k line. instId = %s || bar = %s || before = %s || from = %s" % (
                instId, bar, before, timestamp2datetime(before)))
            continue
        data = resp['data']
        if len(data) == 0:
            print("Empty data: k line. instId = %s || bar = %s || from = %s || to = %s" % (
                instId, bar, timestamp2datetime(before), timestamp2datetime(after)))
            break
            # no more data
        cur -= step
        for line in data:
            ts = int(int(line[0]) / 1000)
            mtime = timestamp2datetime(ts)
            o = float(line[1])
            h = float(line[2])
            l = float(line[3])
            c = float(line[4])
            vol = float(line[5])
            volCcy = float(line[6])
            volCcyQuote = float(line[7])
            confirm = float(line[8])
            if confirm == 0:
                continue
            kline = orm.Schema.Kline(ts=ts,
                                     mtime=mtime,
                                     symbol=instId,
                                     interval=bar,
                                     exchange_name='okx',
                                     o_price=o,
                                     h_price=h,
                                     l_price=l,
                                     c_price=c,
                                     vol=vol,
                                     volCcy=volCcy,
                                     volCcyQuote=volCcyQuote)
            orm.session.merge(kline)
            print("update k line data. mtime=%s||symbol=%s||interval=%s||o_price=%s||c_price=%s||vol=%s"
                  % (mtime, instId, bar, o, c, vol))
        orm.session.commit()
    return


if __name__ == "__main__":
    # update_greedy_fear_index(is_batch=False)
    # update_kline_data_all("BTC-USDT", "1H", common.start_ts, common.start_ts + 86400 * 366)
    update_coin_info()
