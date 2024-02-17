import okx.PublicData as PublicData
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)


if __name__ == "__main__":

    # 获取永续合约当前资金费率
    result = publicDataAPI.get_funding_rate(
        instId="BTC-USD-SWAP",
    )
    print(result)

    result = publicDataAPI.funding_rate_history(
        instId="BTC-USD-SWAP",
    )
    print(result)

    # 获取交易产品历史K线数据
    result = marketDataAPI.get_history_candlesticks(
        instId="BTC-USDT"
    )
    print(result)
