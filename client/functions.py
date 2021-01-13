from aiohttp import ClientSession

url = "http://localhost:8080/"


async def gets():
    async with ClientSession() as session:

        resp1 = await session.get(url)
        print(await resp1.text())

        resp2 = await session.get(url)
        print(await resp2.text())

        resp3 = await session.get(url)
        print(await resp3.text())

        resp4 = await session.get(url)
        print(await resp4.text())

        resp5 = await session.get(url)
        print(await resp5.text())


async def posts():
    async with ClientSession() as session:
        data = {
            'user': "akiles"

        }

        resp = await session.post(url, json=data)
        print(await resp.text())
