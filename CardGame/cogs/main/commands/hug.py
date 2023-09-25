import json, random

from aiohttp.client import ClientSession


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(
            "https://g.tenor.com/v1/random?q=kpophug&key=LIVDSRZULELA"
        ) as r:
            res = json.loads(await r.text())
            rnd = random.randrange(20)
            await ctx.send(res[rnd]["media"][0]["gif"]["url"])
