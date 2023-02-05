from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import (
    get_card_embed,
    get_cooldown,
    show_card,
    check_can_claim,
    get_image,
    try_delete,
)
from datetime import datetime, timezone
import json
import discord
import asyncio


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/epicdrop/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                cardInfos = json.loads(await r.text())["res"]
                starttime = datetime.now(timezone.utc)
                current = 0
                cardInfo, embed, msg = await show_card(
                    ctx,
                    cardInfos[current],
                    [EMOJIS_DROP, EMOJIS_SKIP],
                    "EpicDrop",
                    0xFFAFAF,
                )

                def check(reaction, user):
                    return (
                        reaction.message.id == msg.id
                        and user == ctx.author
                        and str(reaction.emoji) in [EMOJIS_DROP, EMOJIS_SKIP]
                    )

                collected = False
                while (
                    datetime.now(timezone.utc) - starttime
                ).seconds < LONG_COMMAND_TIMEOUT:
                    try:
                        reaction, user = await self.bot.wait_for(
                            "reaction_add", timeout=10, check=check
                        )
                    except asyncio.TimeoutError:
                        a = 1
                    else:
                        msg = await msg.channel.fetch_message(msg.id)
                        if str(reaction.emoji) == EMOJIS_DROP:
                            embed.add_field(name="Owner", value=ctx.author.mention)
                            carduid = json.loads(cardInfos[current])["ID"]
                            async with session.get(
                                f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{carduid}/1"
                            ) as r:
                                await r.text()
                                await msg.edit(embed=embed)
                                await msg.clear_reactions()
                            cardInfos.pop(current)
                            collected = True
                            break
                        elif str(reaction.emoji) == EMOJIS_SKIP:
                            if current < 2:
                                current += 1
                                cardInfo, embed, file = await get_card_embed(
                                    ctx, cardInfos[current], "EpicDrop", 0xFFAFAF
                                )
                                await msg.clear_reactions()
                                await msg.remove_attachments(msg.attachments)
                                await msg.add_files(file)
                                await msg.add_reaction(EMOJIS_DROP)
                                if current < 2:
                                    await msg.add_reaction(EMOJIS_SKIP)
                                await msg.edit(embed=embed)
                                try_delete(file.filename)
                if collected:
                    await asyncio.gather(
                        drop_extra(self, cardInfos[0], ctx),
                        drop_extra(self, cardInfos[1], ctx),
                    )
                else:
                    loseembed = discord.Embed(
                        title="Drop Lost",
                        description="The dropped card has been lost \n due to reaction timeout.",
                        color=0xFF1010,
                    )
                    loseembed.set_author(
                        name=ctx.author.display_name, icon_url=ctx.author.avatar
                    )
                    await msg.delete()
                    await ctx.send(embed=loseembed)


async def drop_extra(self, card, ctx):
    cardInfo, embed, msg = await show_card(
        ctx, card, [EMOJIS_DROP], "Claimable", 0xFBD021
    )

    def check(reaction, user):
        return (
            reaction.message.id == msg.id
            and user != ctx.author
            and user != self.bot.user
            and str(reaction.emoji) == EMOJIS_DROP
        )

    claimed = False
    winner = None
    starttime = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - starttime).seconds < 60:
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=10, check=check
            )
        except asyncio.TimeoutError:
            a = 1
        else:
            if await check_can_claim(self, user, ctx):
                claimed = True
                winner = user
                break
    if claimed:
        embed.add_field(name="Claimed", value=winner.mention)
        await msg.delete()
        carduid = cardInfo["ID"]
        async with ClientSession() as session:
            async with session.get(
                f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}/1"
            ) as r:
                await r.text()
                await ctx.send(embed=embed)
    else:
        loseembed = discord.Embed(
            title="Drop Lost",
            description="The dropped card has been lost \n due to reaction timeout.",
            color=0xFF1010,
        )
        loseembed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        await msg.delete()
        filepath = await get_image(cardInfo["url"])
        file = discord.File(filepath, filename="card.png")
        embed.set_image(url="attachment://card.png")
        await ctx.send(file=file, embed=loseembed)
        try_delete(file.filename)
