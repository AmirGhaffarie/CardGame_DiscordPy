import discord
from aiohttp.client import ClientSession
from utilities.constants import *
from datas import common_emojis


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/balance/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                embed = discord.Embed(title="Balance", color=0x20FF20)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                coins = await r.text()
                emoji = common_emojis.get_emoji("GENERIC_COIN")
                embed.description = f"You have {coins} {emoji} coins."
                await ctx.send(embed=embed)
