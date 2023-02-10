import discord
from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import get_user, get_input_type, get_card, Inputs


async def command(self, ctx, *args):
    async with ClientSession() as session:
        main_card, cards, legit = get_infos(ctx, *args)
        if not legit:
            await ctx.send("Wrong usage of command.")
            return
        all_cards = cards
        all_cards.append(main_card)
        for card in all_cards:
            async with session.get(
                f"{DB_BASE_ADDRESS}/checkcard/{ctx.author.id}/{card}"
            ) as r:
                if r.status == 404:
                    await ctx.send("Player not exist or does not have the card(s).")
                    return
                elif r.status == 210:
                    await ctx.send(await r.text())
                    return
        xp_gains = []
        for card in cards:
            async with session.get(
                f"{DB_BASE_ADDRESS}/fuse/{id}/{main_card}/{card}/"
            ) as r:
                xp_gains.append(await r.text())
        embed = discord.Embed(title="Fuse", color=0xF78589)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed_description = f"{ctx.author.mention} Fused in **{main_card}** the following cards\n"
        for (card, xp) in (cards, xp_gains):
            embed_description += f"{card} - {xp} XP\n"
        embed_description += f"Total {sum(xp_gains)/10} Levels Gained"
        embed.description = embed_description
        await ctx.send(embed=embed)


def get_infos(ctx, *args):
    if len(args) < 2:
        return 0, 0, False
    cards = []
    for i in range(1, len(args)):
        if get_input_type(args[i]) != Inputs.Card:
            return 0, 0, False
        cards[i] = get_card(args[i])
    return get_card(args[1]), cards, True
