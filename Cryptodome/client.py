import aiohttp
import asyncio


async def test_post():
    url = 'http://localhost:8080/data/'
    async with aiohttp.ClientSession() as session:

        resp = await session.post(url, json={"message": "test"})

        text = await resp.text()
        print(f"  status: {resp.status}, text: {text}")


async def test_session():
    url = 'http://localhost:8080/session/'
    async with aiohttp.ClientSession() as session:

        resp = await session.get(url)
        text = await resp.text()
        print(f"  status: {resp.status}, text: {text}")

        resp = await session.get(url)
        text = await resp.text()
        print(f"  status: {resp.status}, text: {text}")

        resp = await session.get(url)
        text = await resp.text()
        print(f"  status: {resp.status}, text: {text}")

        resp = await session.get(url)
        text = await resp.text()
        print(f"  status: {resp.status}, text: {text}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("Test 1: Post")
    loop.run_until_complete(test_post())

    print("Test 2: Session")
    loop.run_until_complete(test_session())
