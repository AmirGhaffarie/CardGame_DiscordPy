import json

import discord
from aiohttp.client import ClientSession

from datas import embeds

from utilities.constants import *
from utilities.functions import (
    get_file,
    get_card,
)


async def command(self, ctx, *args):
    async with ClientSession() as session:
        card, legit = getInfos(ctx, *args)
        if not legit:
            await ctx.send("Wrong use of command.")
            return
        async with session.get(f"{DB_BASE_ADDRESS}/viewcard/{card}") as r:
            if r.status == 404:
                await ctx.send("Card Does not exist.")
            elif r.status == 210:
                await ctx.send(await r.text())
            else:
                cardinfo = json.loads(await r.text())
                embed = discord.Embed(title="View", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                embed.description = embeds.get("VIEW", cardinfo)
                filepath = await get_file(cardinfo["url"])
                file = discord.File(filepath, filename="card.png")
                embed.set_image(url="attachment://card.png")
                await ctx.send(file=file, embed=embed)


def getInfos(ctx, *args):
    if len(args) == 1:
        return get_card(args[0]), True
    return 0, False
