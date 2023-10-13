import json
import random

import discord
from aiohttp import ClientSession

from datas import emojis, embeds
from utilities.constants import *
from utilities.functions import (
    get_cooldown,
    get_image,
    merge_images,
    get_duplicate
)


async def command(self, ctx, *args):
    if len(args) == 0:
        await ctx.send("you need to enter a group name.")
        return
    else:
        groupname = args[0].upper()
        for arg in args[1:]:
            groupname += " " + arg.upper()
    async with ClientSession() as session:
        async with session.get(
            f"{DB_BASE_ADDRESS}/weekly/{ctx.author.id}/{groupname}"
        ) as r:
            if r.status == 404:
                await ctx.send('You need to register with "start" first.')
            elif r.status == 210:
                await ctx.send(f"Wait for {get_cooldown(await r.text())}")
            elif r.status == 220:
                await ctx.send("The group you entered not exists in our cards.")
            elif r.status == 230:
                await ctx.send("The group you entered can't be used with weekly command.")
            else:
                card_infos = json.loads(await r.text())["res"]
                card1 = json.loads(card_infos[0])
                card2 = json.loads(card_infos[1])
                file1path = await get_image(card1["url"])
                file2path = await get_image(card2["url"])
                merged_image = merge_images([file1path, file2path])
                file = discord.File(merged_image, filename="card.png")
                emoji = emojis.get("WEEKLY")
                embed = discord.Embed(title=f"{emoji}Weekly", color=0x9CB6EB)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )

                replacements = card1
                for key,value in card2.items():
                    replacements[key + "2"] = value

                coins_got = random.randint(12, 16)
                replacements["coins"] = str(coins_got)
                embed.set_image(url=f"attachment://card.png")

                card1uid = card1["ID"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card1uid}"
                ) as r:
                    duplicate = await r.text()
                    replacements["duplicate"] = get_duplicate(duplicate)
                card2uid = card2["ID"]

                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card2uid}"
                ) as r2:
                    duplicate = await r2.text()
                    replacements["duplicate2"] = get_duplicate(duplicate)

                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coins_got}"
                ) as r3:
                    await r3.text()

                embed.description = embeds.get("WEEKLY", replacements);

                await ctx.send(file=file, embed=embed)
