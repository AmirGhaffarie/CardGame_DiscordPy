import asyncio
import json
import random
from datetime import datetime, timezone

import discord
from aiohttp import ClientSession

from datas import emojis, embeds
from utilities.constants import *
from utilities.functions import (
    get_card_embed,
    get_cooldown,
    show_card,
    can_claim,
    do_claim,
    get_file,
    get_duplicate,
)


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/epicdrop/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                card_infos = json.loads(await r.text())["res"]
                collected, player = await drop_extra(self, card_infos[0], ctx, False)
                if collected:
                    collected, player = await drop_extra(self, card_infos[1], ctx, player)
                if collected:
                    await drop_extra(self, card_infos[2], ctx, player)


async def drop_extra(self, card, ctx, player):
    drop_emoji = emojis.get(EMOJIS_DROP)
    emoji = emojis.get("LUCKY")
    cardInfo, embed, msg = await show_card(
        ctx, card, [drop_emoji], f"{emoji}Lucky", 0x9CB6EB,"LUCKY1")

    def check(reaction, user):
        return (
            reaction.message.id == msg.id
            and user != self.bot.user
            and str(reaction.emoji) == drop_emoji
        )

    claimed = False
    reacts = []
    start_time = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - start_time).seconds < 8:
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=5, check=check
            )
        except asyncio.TimeoutError:
            pass
        else:
            if ((user == ctx.author and not player)
                    or (user != ctx.author and await can_claim(self, user, ctx))):
                claimed = True
                reacts.append(user)
    player_won = player
    if claimed:
        if not player and reacts.count(ctx.author) > 0:
            winner = ctx.author
            player_won = True
        else:
            winner = random.choice(reacts)

        await msg.delete()
        carduid = cardInfo["ID"]
        await do_claim(self, winner)
        async with ClientSession() as session:
            async with session.get(
                f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}"
            ) as r:
                duplicate = get_duplicate(await r.text())
                cardInfo["duplicate"] = duplicate
                cardInfo["winner"] = winner.mention
                embed.description = embeds.get("CLAIM2", cardInfo)
                filepath = await get_file(cardInfo["url"])
                file = discord.File(filepath, filename="card.png")
                embed.set_image(url="attachment://card.png")
                await ctx.send(file=file, embed=embed)
        return True, player_won
    else:
        lose_embed = discord.Embed(
            title="Drop Lost",
            description="The dropped card has been lost \n due to reaction timeout.",
            color=0x9CB6EB,
        )
        lose_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        await msg.delete()
        await ctx.send(embed=lose_embed)
        return False, player_won
