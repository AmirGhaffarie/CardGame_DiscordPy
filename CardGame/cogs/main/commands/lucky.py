import asyncio
import json
from datetime import datetime, timezone

import discord
from aiohttp import ClientSession

from CardGame.datas import common_emojis
from CardGame.utilities.constants import *
from CardGame.utilities.functions import (
    get_card_embed,
    get_cooldown,
    show_card,
    check_can_claim,
    get_image,
    add_duplicate_to_embed,
)


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
                drop_emoji = common_emojis.get_emoji(EMOJIS_DROP)
                skip_emoji = common_emojis.get_emoji(EMOJIS_SKIP)
                emoji = common_emojis.get_emoji("LUCKY")
                cardInfo, embed, msg = await show_card(
                    ctx,
                    cardInfos[current],
                    [drop_emoji, skip_emoji],
                    f"{emoji}Lucky",
                    0x9CB6EB,
                )

                def check(reaction, user):
                    return (
                        reaction.message.id == msg.id
                        and user == ctx.author
                        and str(reaction.emoji) in [drop_emoji, skip_emoji]
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
                        if str(reaction.emoji) == drop_emoji:
                            embed.add_field(name="Owner", value=ctx.author.mention)
                            carduid = json.loads(cardInfos[current])["ID"]
                            cardrarity = json.loads(cardInfos[current])["rarity_id"]
                            async with session.get(
                                f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{carduid}/{cardrarity}"
                            ) as r:
                                duplicate = await r.text()
                                add_duplicate_to_embed(duplicate, embed)
                                await msg.edit(embed=embed)
                                await msg.clear_reactions()
                            cardInfos.pop(current)
                            collected = True
                            break
                        elif str(reaction.emoji) == skip_emoji:
                            if current < 2:
                                current += 1
                                emoji = common_emojis.get_emoji("LUCKY")
                                cardInfo, embed, file = await get_card_embed(
                                    ctx, cardInfos[current], f"{emoji}Lucky", 0x9CB6EB
                                )
                                await msg.clear_reactions()
                                await msg.remove_attachments(msg.attachments)
                                await msg.add_files(file)
                                await msg.add_reaction(drop_emoji)
                                if current < 2:
                                    await msg.add_reaction(skip_emoji)
                                await msg.edit(embed=embed)
                if collected:
                    await asyncio.gather(
                        drop_extra(self, cardInfos[0], ctx),
                        drop_extra(self, cardInfos[1], ctx),
                    )
                else:
                    loseembed = discord.Embed(
                        title="Drop Lost",
                        description="The dropped card has been lost \n due to reaction timeout.",
                        color=0x9CB6EB,
                    )
                    loseembed.set_author(
                        name=ctx.author.display_name, icon_url=ctx.author.avatar
                    )
                    await msg.delete()
                    await ctx.send(embed=loseembed)


async def drop_extra(self, card, ctx):
    drop_emoji = common_emojis.get_emoji(EMOJIS_DROP)
    emoji = common_emojis.get_emoji("CLAIM")
    cardInfo, embed, msg = await show_card(
        ctx, card, [drop_emoji], f"{emoji}Claimable", 0x9CB6EB
    )

    def check(reaction, user):
        return (
            reaction.message.id == msg.id
            and user != ctx.author
            and user != self.bot.user
            and str(reaction.emoji) == drop_emoji
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
        cardrarity = cardInfo["rarity_id"]
        async with ClientSession() as session:
            async with session.get(
                f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}/{cardrarity}"
            ) as r:
                duplicate = await r.text()
                add_duplicate_to_embed(duplicate, embed)
                await ctx.send(embed=embed)
    else:
        loseembed = discord.Embed(
            title="Drop Lost",
            description="The dropped card has been lost \n due to reaction timeout.",
            color=0x9CB6EB,
        )
        loseembed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        await msg.delete()
        filepath = await get_image(cardInfo["url"])
        file = discord.File(filepath, filename="card.png")
        embed.set_image(url="attachment://card.png")
        await ctx.send(file=file, embed=loseembed)
