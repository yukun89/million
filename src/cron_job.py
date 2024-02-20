# 周期性进行数据拉取

import schedule
import time
import store
import hlog
from hlog import log_info, log_debug, log_error, log_warn


def loop_run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    hlog.init("log/store.log")
    log_info("Starting cron_job")
    schedule.every(8).hours.do(store.update_greedy_fear_index)
    loop_run()
