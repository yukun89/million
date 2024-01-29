#!/bin/python
import sys

import http_utils


def get_greedy_fear_index_history():
    ret_json = http_utils.https_get_request('api.coin-stats.com', '/v2/fear-greed?type=all')
    return ret_json['data']


def get_greedy_fear_index_now():
    ret_json = http_utils.https_get_request('api.coin-stats.com', '/v2/fear-greed?')
    return ret_json['now']


if __name__ == '__main__':
    print('etc.py run as main with path %s' % sys.path)
    ret = get_greedy_fear_index_now()
    print(ret)
    ret = get_greedy_fear_index_history()
    print(ret)
