#!/bin/python
import sys
if __name__ == '__main__':
    import http_utils_
else:
    import api.http_utils_ as http_utils_

def get_greedy_fear_index_history():
    ret_json = http_utils_.https_get_request('api.coin-stats.com', '/v2/fear-greed?type=all')
    return ret_json['data']


def get_greedy_fear_index_now():
    print("http_utils has atributes: %s" % dir(http_utils_))
    ret_json = http_utils_.https_get_request('api.coin-stats.com', '/v2/fear-greed?')
    return ret_json['now']


if __name__ == '__main__':
    print('etc.py run as main with path %s' % sys.path)
    ret = get_greedy_fear_index_now()
    print(ret)
    #ret = get_greedy_fear_index_history()
    print(ret)
