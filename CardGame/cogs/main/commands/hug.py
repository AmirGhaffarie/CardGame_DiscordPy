import asyncio
import json, random

from aiohttp.client import ClientSession


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(
            "https://g.tenor.com/v1/random?q=kpophug&key=LIVDSRZULELA"
        ) as r:
            res = json.loads(await r.text())
            rnd = random.randrange(20)
            if len(args) > 0:
                result = f"{ctx.author.display_name} hugged {args[0]}."
            else:
                result = f"{ctx.author.display_name} hugged air."
            await ctx.send(
                result + "\n" + res["results"][rnd]["media"][0]["gif"]["url"]
            )
