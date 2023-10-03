import asyncio
import json
from datetime import datetime, timezone

import discord
from aiohttp import ClientSession

from datas import emojis, embeds
from utilities.constants import *
from utilities.functions import (
    get_card_embed,
    get_cooldown,
    show_card,
    check_can_claim,
    get_image,
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
                start_time = datetime.now(timezone.utc)
                current = 0
                drop_emoji = emojis.get(EMOJIS_DROP)
                skip_emoji = emojis.get(EMOJIS_SKIP)
                emoji = emojis.get("LUCKY")
                card_info, embed, msg = await show_card(
                    ctx,
                    card_infos[current],
                    [drop_emoji, skip_emoji],
                    f"{emoji}Lucky",
                    0x9CB6EB,
                    "LUCKY1"
                )

                def check(reaction, user):
                    return (
                        reaction.message.id == msg.id
                        and user == ctx.author
                        and str(reaction.emoji) in [drop_emoji, skip_emoji]
                    )

                collected = False
                while (
                    datetime.now(timezone.utc) - start_time
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
                            card = json.loads(card_infos[current])
                            card_uid = card["ID"]
                            async with session.get(
                                f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card_uid}"
                            ) as r:
                                duplicate = get_duplicate(await r.text())
                                card["duplicate"] = duplicate
                                card["owner"] = ctx.author.mention
                                embed.description = embeds.get("LUCKY2", card)
                                await msg.edit(embed=embed)
                                await msg.clear_reactions()
                            card_infos.pop(current)
                            collected = True
                            break
                        elif str(reaction.emoji) == skip_emoji:
                            if current < 2:
                                current += 1
                                emoji = emojis.get("LUCKY")
                                card_info, embed, file = await get_card_embed(
                                    ctx, card_infos[current], f"{emoji}Lucky", 0x9CB6EB
                                )
                                embed.description = embeds.get("LUCKY1", card_info)
                                await msg.clear_reactions()
                                await msg.remove_attachments(msg.attachments)
                                await msg.add_files(file)
                                await msg.add_reaction(drop_emoji)
                                if current < 2:
                                    await msg.add_reaction(skip_emoji)
                                await msg.edit(embed=embed)
                if collected:
                    await drop_extra(self, card_infos[0], ctx)
                    await drop_extra(self, card_infos[1], ctx)
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
    drop_emoji = emojis.get(EMOJIS_DROP)
    emoji = emojis.get("CLAIM")
    cardInfo, embed, msg = await show_card(
        ctx, card, [drop_emoji], f"{emoji}Claimable", 0x9CB6EB,"CLAIM1")

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
        await msg.delete()
        carduid = cardInfo["ID"]
        async with ClientSession() as session:
            async with session.get(
                f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}"
            ) as r:
                duplicate = get_duplicate(await r.text())
                cardInfo["duplicate"] = duplicate
                cardInfo["winner"] = winner.mention
                embed.description = embeds.get("CLAIM2", cardInfo)
                filepath = await get_image(cardInfo["url"])
                file = discord.File(filepath, filename="card.png")
                embed.set_image(url="attachment://card.png")
                await ctx.send(file=file, embed=embed)
    else:
        loseembed = discord.Embed(
            title="Drop Lost",
            description="The dropped card has been lost \n due to reaction timeout.",
            color=0x9CB6EB,
        )
        loseembed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        await msg.delete()
        await ctx.send(embed=loseembed)
