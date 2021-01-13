import asyncio

from functions import gets, posts


loop = asyncio.get_event_loop()
loop.run_until_complete(gets())
loop.run_until_complete(gets())
