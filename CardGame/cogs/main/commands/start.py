from aiohttp.client import ClientSession
from utilities.constants import *


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/register/{ctx.author.id}") as r:
            await ctx.send(await r.text())
