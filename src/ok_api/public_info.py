#/bin/python
import asyncio
import websockets
import time

PUBLIC_URL="wss://ws.okx.com:8443/ws/v5/public"
product_info="""
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

current_price="""
{
    "op": "subscribe",
    "args": [{
        "channel": "tickers",
        "instId": "%s"
    }]
}
"""

kline="""
{
    "op": "subscribe",
    "args": [{
        "channel": "%s",
        "instId": "%s"
    }]
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

def huge_exchange(msg):
    return


asyncio.run(common_api(kline%("candle1m","BTC-USDT"), print))
asyncio.run(common_api(product_info, print))
asyncio.run(common_api(current_price%("BTC-USDT-SWAP"), print))

