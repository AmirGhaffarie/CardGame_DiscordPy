from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown, get_card_embed
from datas import common_emojis
import random
import json


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/daily/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                coinsGot = random.randint(1, 3)
                emoji = common_emojis.get_emoji("GENERIC_COIN")
                cardInfo, embed, file = await get_card_embed(
                    ctx, await r.text(), "Daily", 0xFFAFAF
                )
                embed.add_field(name="Coins", value=f"{coinsGot}{emoji}")
                await ctx.send(file=file, embed=embed)

                carduid = cardInfo["ID"]
                cardrarity = cardInfo["rarity_id"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{carduid}/{cardrarity}"
                ) as r:
                    await r.text()
                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r2:
                    await r2.text()
