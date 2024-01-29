import time
import orm
from api import etc


def timestamp2date(timestamp):
    time_array = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d", time_array)


def update_greedy_fear_index(self, is_batch=False):
    if not is_batch:
        raw_data = etc.get_greedy_fear_index_now()
        daily_greedy_fear_index = orm.Schema.DailyGreedyFearIndex(ts=raw_data["timestamp"],
                                                                  mtime=raw_data["timestamp"],
                                                                  greedy_fear_index=raw_data["greedy_fear_index"])
        orm.session.add(daily_greedy_fear_index)
        orm.session.commit()
    return


if __name__ == "__main__":
    print(timestamp2date(1705622400))
