#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ds import *
from store import *
from hbapi import HuobiServices as api
import threading
import time

#2017年11月1号为计算的起始点
zero_start = 1509465600


def store():
    #Clist = [BTC]
    #Dlist = [Hour]
    #Slist = [5]
    for ct in Clist:
        for duration in Dlist:
            UpdateKline(ct, duration, True)
            for step in Slist:
                UpdateMa(ct, duration, step)
                pass
        UpdateBoll(ct)

class Store (threading.Thread):
    def __init__(self, threadId, name) :
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.status = -1
        pass

    def run(self) :
        self.status = 0
        while True:
            store()
            log_info("sleeping 1H for next round of store")
            time.sleep(600)
        pass

if __name__ == '__main__':
    storer = Store(1, "storer-1")
    storer.start()
    storer.join()

    log_info("main unexpected exit")
    pass
