import json
import discord
from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import get_image, getCard, getUser, getInputType, Inputs, try_delete


async def command(self, ctx, *args):
    async with ClientSession() as session:
        id, card, level, legit = getInfos(ctx, *args)
        if not legit:
            await ctx.send("Wrong use of command.")
            return
        async with session.get(f"{DB_BASE_ADDRESS}/viewcard/{id}/{card}/{level}") as r:
            if r.status == 404:
                await ctx.send("Player not exist or does not have the card.")
            elif r.status == 210:
                await ctx.send(await r.text())
            else:
                cardinfo = json.loads(await r.text())
                embed = discord.Embed(title="View", color=0xB2CCEB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                for key, value in cardinfo.items():
                    if key != "url":
                        embed.add_field(name=key, value=value)
                filepath = await get_image(cardinfo["url"])
                file = discord.File(filepath, filename="card.png")
                embed.set_image(url="attachment://card.png")
                embed.add_field(name="Owner", value=f"<@{id}>")
                await ctx.send(file=file, embed=embed)
                try_delete(file.filename)


def getInfos(ctx, *args):
    if len(args) == 1:
        return ctx.author.id, getCard(args[0]), 0, True
    elif len(args) == 2:
        arg1Type = getInputType(args[0])
        arg2Type = getInputType(args[1])
        if arg1Type == Inputs.User and arg2Type == Inputs.Card:
            return getUser(args[0]), getCard(args[1]), 0, True
        if arg1Type == Inputs.Card and arg2Type == Inputs.Number:
            return ctx.author.id, getCard(args[0]), args[1], True
    elif len(args) == 3:
        arg1Type = getInputType(args[0])
        arg2Type = getInputType(args[1])
        arg3Type = getInputType(args[2])
        if (
            arg1Type == Inputs.User
            and arg2Type == Inputs.Card
            and arg3Type == Inputs.Number
        ):
            return getUser(args[0]), getCard(args[1]), args[2], True
        else:
            return 0, 0, 0, False
    else:
        return 0, 0, 0, False
