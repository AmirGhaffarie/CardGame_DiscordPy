import discord
from aiohttp.client import ClientSession

from CardGame.utilities.constants import *
from CardGame.utilities.functions import get_user, get_input_type, get_card, Inputs


async def command(self, ctx, *args):
    async with ClientSession() as session:
        id, cards, legit = get_infos(ctx, *args)
        if not legit:
            await ctx.send("Wrong usage of command.")
            return
        for card in cards:
            async with session.get(
                f"{DB_BASE_ADDRESS}/checkcard/{ctx.author.id}/{card}"
            ) as r:
                if r.status == 404:
                    await ctx.send("Player not exist or does not have the card.")
                    return
                elif r.status == 210:
                    await ctx.send(await r.text())
                    return
        for card in cards:
            async with session.get(
                f"{DB_BASE_ADDRESS}/giftcard/{ctx.author.id}/{id}/{card}"
            ) as r:
                await r.text()
        embed = discord.Embed(title="Gift", color=0x9CB6EB)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed_description = f"{ctx.author.mention} gifted <@{id}> the following cards\n"
        for card in cards:
            embed_description += f"{card}\n"
        embed.description = embed_description
        await ctx.send(embed=embed)


def get_infos(ctx, *args):
    if len(args) < 2 or get_input_type(args[0]) != Inputs.User:
        return 0, 0, False
    cards = []
    for i in range(1, len(args)):
        if get_input_type(args[i]) != Inputs.Card:
            return 0, 0, False
        cards.append(get_card(args[i]))
    return get_user(args[0]), cards, True
