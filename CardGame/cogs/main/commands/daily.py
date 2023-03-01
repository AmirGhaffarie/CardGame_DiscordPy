from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown, get_card_embed , add_duplicate_to_embed
from datas import common_emojis
import random

async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/daily/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:

                duplicate = False

                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{carduid}/{cardrarity}"
                ) as r2:
                    duplicate = bool(await r2.text())
                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r3:
                    await r3.text()

                coinsGot = random.randint(1, 3)
                emoji = common_emojis.get_emoji("GENERIC_COIN")
                emoji2 = common_emojis.get_emoji("DAILY")
                cardInfo, embed, file = await get_card_embed(
                    ctx, await r.text(), f"{emoji2}Daily", 0xFFAFAF
                )

                add_duplicate_to_embed(duplicate, embed)

                embed.add_field(name="Coins", value=f"{coinsGot}{emoji}")
                await ctx.send(file=file, embed=embed)

                carduid = cardInfo["ID"]
                cardrarity = cardInfo["rarity_id"]
