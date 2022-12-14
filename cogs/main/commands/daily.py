from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown, show_card
import random
import json


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DJANGO_SERVER_ADDRESS}/daily/{ctx.author.id}") as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            else:
                coinsGot = random.randint(1, 3)
                respond = await r.text()
                items = json.loads(respond)
                items["Coins"] = str(coinsGot) + EMOJIS_COIN
                items = json.dumps(items)
                cardInfo, embed, msg = await show_card(
                    ctx, items, [], "Daily", 0xFFAFAF
                )
                carduid = cardInfo["ID"]
                async with session.get(
                    f"{DJANGO_SERVER_ADDRESS}/addcard/{ctx.author.id}/{carduid}/1"
                ) as r:
                    await r.text()
                async with session.get(
                    f"{DJANGO_SERVER_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r2:
                    await r2.text()
