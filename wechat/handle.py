# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 21:24:18 2017

@author: Selay
"""
import requests
import web
import json
from hlog import *
from redis_cli import *
import hashlib
import receive
import reply
import robot

class Handle(object):
    def __init__(self):
        self.token_ = "hello_ykhuang"
    def POST(self):
        try:
            webData = web.data()
            log_info("Handle Post webdata is %s"%webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                recContent  = recMsg.Content.decode('utf8')
                #print(replyContent.decode('utf8'))
                print("Input", recContent)#str-utf8类型
                replyContent = robot.get_response(recContent)
                print("Output", replyContent)#str-utf8类型
                replyMsg = reply.TextMsg(toUser, fromUser, replyContent)
                return replyMsg.send()
            else:
                print("hold")
                return "success"
        except Exception as e:
            print(e)
            return  e
    def GET(self):
        try:
            data = web.input()
            if data is None:
                print('Failed to get data from web.input. None Data')
                return 'Null data'
            if len(data) == 0 or data.signature is None or data.timestamp is None:
                print("Unexpected data [%s]"%data)
                return "Unexpected data [%s]"%(data)
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            #token,ex = get_wechat_token_info()

            list1 = [self.token_, timestamp, nonce]
            list1.sort()

            sha1 = hashlib.sha1()
            for element in list1:
                sha1.update(element.encode("utf8"))
            hashcode = sha1.hexdigest()
            print("handle/GET func: token=%s, timestamp=%s, nonce=%s, hashcode=%s, signature=%s "%(self.token_, timestamp, nonce, hashcode, signature))
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as e:
            tmp = web.data()
            print("Failed to get data(%s) from we input. exception is %s"%(tmp, str(e)))
            return str(e)

