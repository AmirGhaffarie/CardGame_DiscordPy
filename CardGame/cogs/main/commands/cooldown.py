from aiohttp.client import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown
import json
import discord
from datas import common_emojis


async def command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/cds/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                val = ""
                items = json.loads(await r.text())
                for key, value in items.items():
                    val += f"{common_emojis.get_emoji(key.upper())} {key} : {get_cooldown(value)}\n"

                embed = discord.Embed(title="Cooldowns", color=0x000000)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                embed.set_thumbnail(ICON_TOPRIGHT)
                embed.description = val
                await ctx.send(embed=embed)
