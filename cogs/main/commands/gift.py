import discord
from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import getUser, getInputType, Inputs


async def command(self, ctx, *args):
    async with ClientSession() as session:
        id, cards, legit = getInfos(ctx, *args)
        if not legit:
            await ctx.send("Wrong usage of command.")
            return
        for card, count in cards.items():
            async with session.get(
                f"{DJANGO_SERVER_ADDRESS}/checkcard/{ctx.author.id}/{card}/{count}"
            ) as r:
                if r.status == 404:
                    await ctx.send("Player not exist or does not have the card.")
                    return
                elif r.status == 210:
                    await ctx.send(await r.text())
                    return
        for card, count in cards.items():
            async with session.get(
                f"{DJANGO_SERVER_ADDRESS}/giftcard/{ctx.author.id}/{id}/{card}/{count}"
            ) as r:
                await r.text()
        embed = discord.Embed(title="Gift", color=0xF78589)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed_description = f"{ctx.author.mention} gifted <@{id}> the following cards\n"
        for card, count in cards.items():
            embed_description += f"{card} - {count}\n"
        embed.description = embed_description
        await ctx.send(embed=embed)


def getInfos(ctx, *args):
    if len(args) < 3 or len(args) % 2 != 1 or getInputType(args[0]) != Inputs.User:
        return 0, 0, False
    cards = {}
    for i in range(1, len(args), 2):
        if (
            getInputType(args[i]) != Inputs.Card
            or getInputType(args[i + 1]) != Inputs.Number
        ):
            return 0, 0, False
        cards[args[i]] = args[i + 1]
    return getUser(args[0]), cards, True
