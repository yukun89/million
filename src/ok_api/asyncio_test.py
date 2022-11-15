#/bin/python
import asyncio
import websockets
import time


async def func1():
    while True:
        print("1")
        await asyncio.sleep(1)

async def func2():
    while True:
        print("1")
        await asyncio.sleep(1)

#
asyncio.run(fun())

