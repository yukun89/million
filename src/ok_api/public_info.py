# /bin/python
import asyncio
import websockets
import time
import json

if __name__ == "__main__":
    from ..iowapper import rds
else:
    from iowapper import rds

# 获取ok上的公共信息：非私有信息，相对安全，不需要API key

PUBLIC_URL = "wss://ws.okx.com:8443/ws/v5/public"
product_info = """
{
  "op": "subscribe",
  "args":   [
    {
      "channel" : "instruments",
      "instType": "SWAP"
    }
  ]
}
"""

current_price = """
{
    "op": "subscribe",
    "args": [{
        "channel": "tickers",
        "instId": "%s"
    }]
}
"""

kline = """
{
    "op": "subscribe",
    "args": [{
        "channel": "%s",
        "instId": "%s"
    }]
}
"""

liquidation = """
{
  "op": "subscribe",
  "args": [
    {
      "channel": "liquidation-orders",
      "instType": "SWAP"
    }
  ]
}
"""


async def common_api(send_info, handler):
    try:
        async with websockets.connect(PUBLIC_URL) as websocket:
            await websocket.send(send_info)
            while True:
                recv_msg = await websocket.recv()
                handler(recv_msg)
    except websockets.exceptions.ConnectionClosedError as e:
        print("connection closed error")
    except Exception as e:
        print(e)


def handle_huge_liquidation(msg):
    msg = json.loads(msg)
    if msg.get('data') is None:
        return
    instId = msg['data'][0]['instId']

    # {'bkLoss': '0', 'bkPx': '0.03728', 'ccy': '', 'posSide': 'long', 'side': 'sell', 'sz': '187', 'ts': '1708401881098'}
    body = msg['data'][0]['details'][0]
    posSide = body['posSide']
    sz = int(body['sz'])
    price = float(body['bkPx'])
    side = body['side']
    ts = int(body['ts'])
    cur_min = int(ts / 60) * 60
    lqd_key = f"lqd__{instId}__{side}__{posSide}__{cur_min}"
    rds.g_redis.incrby(lqd_key, sz)
    rds.g_redis.expire(lqd_key, 86400)
    value = rds.g_redis.get(lqd_key)
    if value is not None and int(value) > 10000:
        print("liquidation : key=%s || sz = %s || %d" % (time.ctime(), lqd_key, value))

    return


if __name__ == "__main__":
    # asyncio.run(common_api(kline % ("candle1m", "BTC-USDT"), print))
    # asyncio.run(common_api(product_info, print))
    # 获取实时价格
    # asyncio.run(common_api(current_price % "BTC-USDT-SWAP", print))
    asyncio.run(common_api(liquidation, handle_huge_liquidation))
