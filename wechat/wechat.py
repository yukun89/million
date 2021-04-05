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
from handle import Handle

# 字典allusers用于存储 由 索引名和openID构成的键值对
# 微信关注‘测试号’时，会生成openID用于与对应微信账号通讯
# 索引名 是为了便于自己识别和管理而对openID起的别名
allusers = {'大大':'eXIuShYFO7tghjb_4YWA'}


def usersto(users = None):
    if users == None:
        return allusers['大大']
    elif users == "All":
        return ','.join(set(allusers.values()))
    else:
        if isinstance(users,list):
            usersinfo = []
            for user in users:
                usersinfo.append(allusers[user])
            return ','.join(set(usersinfo))
        else:
            print("'users' must be a list!")
            return

def json_post_data_generator(content='Hi!你好！',users = None):
    msg_content = {}
    msg_content['content'] = content
    post_data = {}
    post_data['text'] = msg_content
    post_data['touser'] = "%s" % usersto(users)
    post_data['toparty'] = ''
    post_data['msgtype'] = 'text'
    post_data['agentid'] = '9'
    post_data['safe'] = '0'
    #由于字典格式不能被识别，需要转换成json然后在作post请求
    #注：如果要发送的消息内容有中文的话，第三个参数一定要设为False
    return json.dumps(post_data)

# 需将此处的APPID,APPSECRET换为自己‘测试号管理’页面内显示的内容
def appInfos():
    APPID = "wx246c22ddfe906f57"
    APPSECRET = "77690fa89405e7fa2ac6657e37804b66"
    return (APPID,APPSECRET)

# 从微信公众号平台获取token信息
def get_wechat_token_info():
    val = g_redis.get('wechat_token')
    if val is not None:
        return val, 300

    APPInfo = appInfos()
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % APPInfo)
    log_debug("visit wechat api to get token. Accessing %s" %r.url)
    js =  r.json()
    if "errcode" not in js:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
        g_redis.set('wechat_token', access_token, ex=int(expires_in) - 300)
        print("get token=%s, will expire in %s second"%(access_token, expires_in))
    else:
        print("Can not get the access_token. content=[%s]"%js)
        quit()
    return access_token, expires_in

post_url_freshing = ['']

def post_url():
    access_token,expires_in = get_wechat_token_info()
    print("token expires_in:%s" % expires_in)
    timer = threading.Timer((expires_in-200),post_url)
    timer.start()
    post_url_freshing[0] = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' %access_token

#TODO
#post_url()

def sender(text_str,user_lis = None):
    posturl = post_url_freshing[0]
    post_data = json_post_data_generator(content=text_str,users = user_lis)
    r = requests.post(posturl,data=post_data)
    result = r.json()
    if result["errcode"] == 0:
        print("Sent successfully")
    else:
        print("Failed to send err:%s"%result["errmsg"])


urls = (
    '/wx', 'Handle',
)

if __name__ == "__main__":
    # text_str = "你好"
    # user_lis = None
    # sender(text_str,user_lis)
    app = web.application(urls, globals())
    web.internalerror = web.debugerror
    app.run()
