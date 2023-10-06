import discord
from aiohttp.client import ClientSession

from datas import emojis, embeds
from utilities.constants import *
from utilities.functions import get_user


async def command(self, ctx,  *args):
    async with ClientSession() as session:
        user = ctx.author.id
        if len(args) > 0:
            user = get_user(args[0])
        async with session.get(f"{DB_BASE_ADDRESS}/balance/{user}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            else:
                emoji = emojis.get("WALLET")

                embed = discord.Embed(title=f"{emoji}Balance", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )
                coins = await r.text()
                content = {"coins": coins}
                embed.description = embeds.get("BALANCE", content)
                await ctx.send(embed=embed)
