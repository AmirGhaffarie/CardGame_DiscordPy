from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import get_image, get_cooldown, show_card
import discord
import random
from asyncio import sleep


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/drop/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                cardInfo, embed, msg = await show_card(
                    ctx, await r.text(), [EMOJIS_DROP], "Drop", 0xFFAFAF
                )
                await sleep(DROP_TIMEOUT)
                msg = await msg.channel.fetch_message(msg.id)
                ra = list(filter(lambda x: str(x.emoji) == EMOJIS_DROP, msg.reactions))[
                    0
                ]
                users = [user async for user in ra.users(limit=100)]
                users = [u for u in users if u.id != self.bot.user.id]
                if len(users) < 2:
                    loseembed = discord.Embed(
                        title="Drop Lost",
                        description="The dropped card has been lost \n due to not enough reactions.",
                        color=0xFF1010,
                    )
                    loseembed.set_author(
                        name=ctx.author.display_name, icon_url=ctx.author.avatar
                    )
                    await msg.delete()
                    await ctx.send(embed=loseembed)
                else:
                    winner = random.choice(users)
                    embed.add_field(name="Winner", value=winner.mention)
                    await msg.delete()
                    carduid = cardInfo["ID"]
                    cardrarity = cardInfo["rarity_id"]
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/addcard/{winner.id}/{carduid}/{cardrarity}"
                    ) as r:
                        await r.text()
                        filepath = await get_image(cardInfo["url"])
                        file = discord.File(filepath, filename="card.png")
                        embed.set_image(url="attachment://card.png")
                        await ctx.send(file=file, embed=embed)
