# /bin/python
import asyncio
import websockets
import time
import json
#获取ok上的公共信息：非私有信息，相对安全，不需要API key

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

    body = msg['data'][0]['details'][0]
    posSide = body['posSide']
    sz = int(body['sz'])
    if sz > 1000:
        print("liquidation %s: instId=%s || posSide=%s || sz = %s" % (time.ctime(), instId, posSide, sz))
    return



if __name__ == "__main__":
    #asyncio.run(common_api(kline % ("candle1m", "BTC-USDT"), print))
    #asyncio.run(common_api(product_info, print))
    #获取实时价格
    #asyncio.run(common_api(current_price % "BTC-USDT-SWAP", print))
    asyncio.run(common_api(liquidation, handle_huge_liquidation))

