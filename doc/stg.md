
策略

## 策略列表

### Black Swan

黑天鹅策略：在大盘无明显异常的情况下，某个币的价格出现了异常波动，此时去填充价格真空，获取额外收益。

#### 价格下探策略

大盘无异常定义：
   最近一日贪婪恐惧指数-greedy_fear_index: 35~48
   BTC最近24H跌幅-price_change_ratio_24H: > -5%
    
过滤条件：
   热度排名-hot_rank: [5, 1000)
   市值-market_value: (0.1, 20) billion
   price_change_ratio_24H < 0.3

 