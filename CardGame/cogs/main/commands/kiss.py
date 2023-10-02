import asyncio
import json, random

import discord
from aiohttp.client import ClientSession


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(
            "https://g.tenor.com/v1/random?q=kpopkiss&key=LIVDSRZULELA"
        ) as r:
            res = json.loads(await r.text())
            rnd = random.randrange(20)
            embed = discord.Embed(title=f"Kiss", color=0x9CB6EB)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            if len(args) > 0:
                embed.description = f"{ctx.author.mention} kissed {args[0]}."
            else:
                embed.description = f"{ctx.author.mention} blown away a kiss."

            embed.set_image(url=res["results"][rnd]["media"][0]["gif"]["url"])

            await ctx.send(embed=embed)
