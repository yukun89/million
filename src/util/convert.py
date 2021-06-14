#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

def timestamp2dstring(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d")
        return str1
    except Exception as e:
        print("convert exception: %s"%(str(e)))
    return ''

def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return str1
    except Exception as e:
        print("convert exception: %s"%(str(e)))
    return ''
