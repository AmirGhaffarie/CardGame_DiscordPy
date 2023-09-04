import json

import discord
from aiohttp.client import ClientSession

from CardGame.datas import common_emojis
from CardGame.utilities.constants import *
from CardGame.utilities.functions import get_cooldown


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

                embed = discord.Embed(title="Cooldowns", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                embed.set_thumbnail(url=ICON_TOPRIGHT)
                embed.description = val
                await ctx.send(embed=embed)
