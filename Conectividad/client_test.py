import aiohttp
import asyncio

url = 'http://httpbin.org/get'


async def main1():
    # Forma utilizada en el ejemplo principal
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print("main 1")
            print(resp.status)
            print(await resp.text())


async def main2():
    # Mismo ejemplo reescrito
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        print("main 2")
        print(response.status)
        print(await response.text())


async def main3():
    session = aiohttp.ClientSession()

    resp = await session.get(url)
    print("main 3")
    print(resp.status)
    print(await resp.text())

    await session.close()


async def function(session, message):
    async with session.get(url) as resp:
        print(message)
        print(resp.status)
        print(await resp.text())


async def main4():
    session = aiohttp.ClientSession()

    await function(session, "main 4")

    await session.close()


async def all_main():

    await asyncio.gather(
        main1(),
        main2(),
        main3(),
        main4()
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(all_main())
