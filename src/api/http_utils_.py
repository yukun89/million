#!/bin/python
import json
import http.client
import ssl
import urllib
import urllib.parse
import urllib.request
import requests
import sys


def http_get_request(url, params, add_to_headers=None, debug=False):
    if params is None:
        params = {}
    if debug:
        print("http_get_request url=%s || params=%s" % (url, params))
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    post_data = urllib.parse.urlencode(params)
    response = requests.get(url, post_data, headers=headers, timeout=5, verify=False)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" % (response.text, e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    post_data = json.dumps(params)
    response = requests.post(url, post_data, headers=headers, timeout=10)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" % (response.text, e))
        return


def https_get_request(url, path,  add_to_headers=None, debug=False):
    if debug:
        print("comrequest_in: https_get_request url=%s || path=%s " % (url, path))
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    context = ssl.create_default_context()
    conn = http.client.HTTPSConnection(url, context=context)  # url=www.baidu.com

    conn.request('GET', path, None, headers=headers)
    response = conn.getresponse()
    try:
        if response.status == 200:
            return json.loads(response.read())
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" % (response.reason, e))
        return


# https: https://blog.51cto.com/u_16213304/7588268
# json:https://www.yzktw.com.cn/post/1144316.html
if __name__ == '__main__':
    DEBUG = 1
    ret_json = https_get_request('api.coin-stats.com', '/v2/fear-greed?', None, True)
    print(ret_json['now'])
    ret_json = https_get_request('api.coin-stats.com', '/v2/fear-greed?type=all', None, True)
    print(ret_json['data'])
    print(sys.path)
