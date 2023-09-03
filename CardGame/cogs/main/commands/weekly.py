import random
from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import (
    get_cooldown,
    get_image,
    merge_images,
    add_duplicate_to_embed,
    add_coins_to_embed,
)
import json
import discord
from datas import common_emojis


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
            else:
                cardInfos = json.loads(await r.text())["res"]
                card1 = json.loads(cardInfos[0])
                card2 = json.loads(cardInfos[1])
                file1path = await get_image(card1["url"])
                file2path = await get_image(card2["url"])
                merged_image = merge_images([file1path, file2path])
                file = discord.File(merged_image, filename="card.png")
                emoji = common_emojis.get_emoji("WEEKLY")
                embed = discord.Embed(title=f"{emoji}Weekly", color=0xFF00FF)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )

                embed.description = card1["CardDescription"]

                coinsGot = random.randint(12, 16)

                embed.set_image(url=f"attachment://card.png")
                card1uid = card1["ID"]
                card1rarity = card1["rarity_id"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card1uid}/{card1rarity}"
                ) as r:
                    duplicate = await r.text()
                    add_duplicate_to_embed(duplicate, embed)

                embed.description += "\n\n" + card2["CardDescription"]
                card2uid = card2["ID"]
                card2rarity = card2["rarity_id"]

                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card2uid}/{card2rarity}"
                ) as r:
                    duplicate = await r.text()
                    add_duplicate_to_embed(duplicate, embed)

                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r2:
                    await r2.text()
                add_coins_to_embed(coinsGot, embed)
                await ctx.send(file=file, embed=embed)
