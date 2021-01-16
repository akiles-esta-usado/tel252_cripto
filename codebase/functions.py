

#url = "http://40.87.109.190"
url = "http://localhost:8080/"

k_pub_ca = 2
id_0 = 1234


async def gets(session):

    resp1 = await session.get(url)
    print(await resp1.text())
    print(resp1.cookies)

    resp2 = await session.get(url)
    print(await resp2.text())
    print(resp1.cookies)

    resp3 = await session.get(url)
    print(await resp3.text())
    print(resp1.cookies)

    resp4 = await session.get(url)
    print(await resp4.text())
    print(resp1.cookies)

    resp5 = await session.get(url)
    print(await resp5.text())
    print(resp1.cookies)


async def posts(session):
    data = {
        'user': "akiles"
    }

    resp = await session.post(url, json=data)
    print(await resp.text())
