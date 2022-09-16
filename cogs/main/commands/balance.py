import discord
from aiohttp.client import ClientSession
from utilities.constants import *


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DJANGO_SERVER_ADDRESS}/balance/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                embed = discord.Embed(title="Balance", color=0x20FF20)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                coins = await r.text()
                embed.description = f"You have {coins} {EMOJIS_COIN} coins."
                await ctx.send(embed=embed)
