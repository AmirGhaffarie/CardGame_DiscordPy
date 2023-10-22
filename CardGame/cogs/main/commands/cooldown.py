import json

import discord
from aiohttp.client import ClientSession

from datas import emojis
from utilities.constants import *
from utilities.functions import get_cooldown


async def cd_command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/cds/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                val = ""
                items = json.loads(await r.text())
                for key, value in items.items():
                    val += f"{emojis.get(key.upper())} {key} : {get_cooldown(value)}\n"

                embed = discord.Embed(title="Cooldown", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                embed.set_thumbnail(url=ICON_TOPRIGHT)
                embed.description = val
                await ctx.send(embed=embed)


async def ccd_command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/cds/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                valids = ["Drop", "Lucky", "Daily", "Weekly", "Claim"]
                await show_partial_cd(ctx, r, valids)


async def show_partial_cd(ctx, r, valids):
    val = ""
    items = json.loads(await r.text())
    for key, value in items.items():
        if key in valids:
            val += f"{emojis.get(key.upper())} {key} : {get_cooldown(value)}\n"
    embed = discord.Embed(title="Cooldown", color=0x9CB6EB)
    embed.set_author(
        name=ctx.author.display_name, icon_url=ctx.author.avatar
    )
    embed.set_thumbnail(url=ICON_TOPRIGHT)
    embed.description = val
    await ctx.send(embed=embed)


async def scd_command(self, ctx):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/cds/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                valids = ["Stargaze", "Discover"]
                await show_partial_cd(ctx, r, valids)
