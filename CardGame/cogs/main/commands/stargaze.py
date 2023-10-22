import random
import discord

from aiohttp import ClientSession

from datas import embeds
from utilities.constants import *
from utilities.functions import (
    get_cooldown,
)


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/stargaze/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                coins_got = random.randint(5, 10)

                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coins_got}"
                ) as r1:
                    await r1.text()

                embed = discord.Embed(title=f"Stargaze", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )

                content = {"coins": coins_got}
                embed.description = embeds.get("STARGAZE", content)

                await ctx.send(embed=embed)
