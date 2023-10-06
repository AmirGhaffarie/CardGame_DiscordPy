import discord

from aiohttp import ClientSession

from datas import discoveries
from utilities.constants import *
from utilities.functions import (
    get_cooldown,
)


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/daily/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                amount, desc = discoveries.get()

                if amount > 0:
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{amount}"
                    ) as r1:
                        await r1.text()

                embed = discord.Embed(title=f"Discover", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )

                embed.description = desc

                await ctx.send(embed=embed)
