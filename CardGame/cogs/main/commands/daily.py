import random

from aiohttp import ClientSession

from datas import common_emojis
from utilities.constants import *
from utilities.functions import (
    get_cooldown,
    get_card_embed,
    add_duplicate_to_embed,
    add_coins_to_embed,
)


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/daily/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                coinsGot = random.randint(1, 3)
                emoji2 = common_emojis.get_emoji("DAILY")
                cardInfo, embed, file = await get_card_embed(
                    ctx, await r.text(), f"{emoji2}Daily", 0x9CB6EB
                )
                duplicate = False
                carduid = cardInfo["ID"]
                cardrarity = cardInfo["rarity_id"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{carduid}/{cardrarity}"
                ) as r2:
                    duplicate = await r2.text()
                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r3:
                    await r3.text()

                add_duplicate_to_embed(duplicate, embed)
                add_coins_to_embed(coinsGot, embed)

                await ctx.send(file=file, embed=embed)
