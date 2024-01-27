#!/bin/python
from .utils import *
import json
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/transactions-on-the-bitcoin-network-daily
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/number-of-active-addresses-on-the-bitcoin-network-7dma
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/number-of-new-addresses-on-the-bitcoin-network-7dma
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/bitcoins-adjusten-on-chain-volume-daily
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/bitcoin-miner-revenue-daily
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/bitcoin-share-of-transaction-fee-from-total-miner-revenue-monthly
#https://www.theblock.co/api/charts/chart/on-chain-metrics/bitcoin/bitcoin-addresses-with-balance-over-x

class TheBlock(object):
    def __init__(self):
        self.http_prefix_="https://www.theblock.co/api/charts/chart/on-chain-metrics/"
        self.key_map_={'BTC':'bitcoin'}
        return

#[{'Timestamp': 1668556800, 'Result': 266171.14285714284}]
    def get_daily_transactions(self, symbol):
        usymbol=self.key_map_.get(symbol, 'BTC')
        url=self.http_prefix_+usymbol+"/transactions-on-the-%s-network-daily"%usymbol
        resp = http_get_request(url, params={}, add_to_headers=None, debug=True)
        data = resp['chart']['jsonFile']['Series']['Daily Transactions']['Data']
        return data 

    def get_active_address(self, symbol):
        usymbol=self.key_map_.get(symbol, 'BTC')
        url=self.http_prefix_+usymbol+"number-of-active-addresses-on-the-%s-network-7dma"%usymbol
        resp = http_get_request(url, params={}, add_to_headers=None, debug=True)
        data = resp['chart']['jsonFile']['Series']['Daily Transactions']['Data']
        return data

    def get_new_address(self, symbol):
        usymbol=self.key_map_.get(symbol, 'BTC')
        url=self.http_prefix_+usymbol+"number-of-new-addresses-on-the-%s-network-7dma"%usymbol
        resp = http_get_request(url, params={}, add_to_headers=None, debug=True)
        data = resp['chart']['jsonFile']['Series']['Daily Transactions']['Data']
        return data

    def get_adjusten_on_chain_volume(self, symbol):
        return

if __name__ == '__main__':
    theblock = TheBlock()
    print(theblock.get_daily_transactions('BTC'))
