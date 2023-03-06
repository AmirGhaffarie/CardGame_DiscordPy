import json
import discord
from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import (
    get_image,
    get_card,
    get_user,
    get_input_type,
    Inputs,
)


async def command(self, ctx, *args):
    async with ClientSession() as session:
        id, card, level, legit = getInfos(ctx, *args)
        if not legit:
            await ctx.send("Wrong use of command.")
            return
        async with session.get(f"{DB_BASE_ADDRESS}/viewcard/{id}/{card}") as r:
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
                embed.description = cardinfo["CardDescription"]
                filepath = await get_image(cardinfo["url"])
                file = discord.File(filepath, filename="card.png")
                embed.set_image(url="attachment://card.png")
                embed.add_field(name="Owner", value=f"<@{id}>")
                await ctx.send(file=file, embed=embed)


def getInfos(ctx, *args):
    if len(args) == 1:
        return ctx.author.id, get_card(args[0]), 0, True
    elif len(args) == 2:
        arg1Type = get_input_type(args[0])
        arg2Type = get_input_type(args[1])
        if arg1Type == Inputs.User and arg2Type == Inputs.Card:
            return get_user(args[0]), get_card(args[1]), 0, True
        if arg1Type == Inputs.Card and arg2Type == Inputs.Number:
            return ctx.author.id, get_card(args[0]), args[1], True
    elif len(args) == 3:
        arg1Type = get_input_type(args[0])
        arg2Type = get_input_type(args[1])
        arg3Type = get_input_type(args[2])
        if (
            arg1Type == Inputs.User
            and arg2Type == Inputs.Card
            and arg3Type == Inputs.Number
        ):
            return get_user(args[0]), get_card(args[1]), args[2], True
        else:
            return 0, 0, 0, False
    else:
        return 0, 0, 0, False
