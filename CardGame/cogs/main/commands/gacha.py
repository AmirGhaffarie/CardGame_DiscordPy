import random
from asyncio import sleep

import discord
from aiohttp import ClientSession

from datas import emojis
from utilities.constants import *
from utilities.functions import (
    get_image,
    get_cooldown,
    show_card,
    add_duplicate_to_embed,
)


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/drop/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                drop_emoji = emojis.get(EMOJIS_DROP)
                emoji = emojis.get("Drop")
                card_info, embed, msg = await show_card(
                    ctx, await r.text(), [drop_emoji], f"{emoji}Drop", 0x9CB6EB
                )
                await sleep(DROP_TIMEOUT)
                msg = await msg.channel.fetch_message(msg.id)
                ra = list(filter(lambda x: str(x.emoji) == drop_emoji, msg.reactions))[
                    0
                ]
                users = [user async for user in ra.users(limit=100)]
                users = [u for u in users if u.id != self.bot.user.id]
                if len(users) < 1:
                    lose_embed = discord.Embed(
                        title="Drop Lost",
                        description="The dropped card has been lost \n due to no reactions.",
                        color=0x9CB6EB,
                    )
                    lose_embed.set_author(
                        name=ctx.author.display_name, icon_url=ctx.author.avatar
                    )
                    await msg.delete()
                    await ctx.send(embed=lose_embed)
                else:
                    winner = random.choice(users)
                    embed.add_field(name="Winner", value=winner.mention)
                    await msg.delete()
                    carduid = card_info["ID"]
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}"
                    ) as r:
                        duplicate = await r.text()
                        filepath = await get_image(card_info["url"])
                        file = discord.File(filepath, filename="card.png")
                        embed.set_image(url="attachment://card.png")
                        add_duplicate_to_embed(duplicate, embed)
                        await ctx.send(file=file, embed=embed)
