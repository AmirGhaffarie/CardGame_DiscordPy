from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown
import json
import discord


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DJANGO_SERVER_ADDRESS}/cds/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                val = ""
                items = json.loads(await r.text())
                for key, value in items.items():
                    val += f"{key} : {get_cooldown(value)}\n"

                embed = discord.Embed(title="Cooldowns", color=0x000000)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                embed.description = val
                await ctx.send(embed=embed)
