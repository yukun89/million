#周期性进行数据拉取

import schedule
import time
import store

def loop_run():
    while True:
        schedule.run_pending()
        time.sleep()

if __name__ == "__main":
    schedule.every(3).hours.do(store.update_greedy_fear_index)
    loop_run()
