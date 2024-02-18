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
    print("http_utils has attributes: %s" % dir(http_utils_))
    ret_json = http_utils_.https_get_request('api.coin-stats.com', '/v2/fear-greed?')
    return ret_json['now']


def get_market_data(symbol_id):
    """
    id: btc > bitcoin
    id can be get using get_coin_list
    response:
    [
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
    "current_price": 51587,
    "market_cap": 1012739327675,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 1083352336119,
    "total_volume": 21386101509,
    "high_24h": 52021,
    "low_24h": 50675,
    "price_change_24h": 39.86,
    "price_change_percentage_24h": 0.07733,
    "market_cap_change_24h": -106850531.92004395,
    "market_cap_change_percentage_24h": -0.01055,
    "circulating_supply": 19631218,
    "total_supply": 21000000,
    "max_supply": 21000000,
    "ath": 69045,
    "ath_change_percentage": -25.28296,
    "ath_date": "2021-11-10T14:24:11.849Z",
    "atl": 67.81,
    "atl_change_percentage": 75978.70118,
    "atl_date": "2013-07-06T00:00:00.000Z",
    "roi": null,
    "last_updated": "2024-02-18T13:21:30.450Z"
  }
]
    """
    ret_json = http_utils_.https_get_request('api.coingecko.com',
                                             '/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en&ids=%s' % symbol_id)
    return ret_json


def get_coin_list():
    """
    [
    {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin"
    }...
    ]
    """
    ret_json = http_utils_.https_get_request('api.coingecko.com', '/api/v3/coins/list?')
    return ret_json


if __name__ == '__main__':
    print('etc.py run as main with path %s' % sys.path)
    ret = get_greedy_fear_index_now()
    print(ret)
    # ret = get_greedy_fear_index_history()
    # print(ret)
    #ret = get_market_data("bitcoin")
    ret = get_coin_list()
    print(ret)
