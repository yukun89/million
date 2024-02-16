# /bin/python
import asyncio


async def func1():
    while True:
        print("1")
        await asyncio.sleep(1)


async def func2():
    while True:
        print("1")
        await asyncio.sleep(1)


#
if __name__ == "__main__":
    asyncio.run(func1())
