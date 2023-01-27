import random
from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import get_cooldown, get_image, get_tempfilename, show_card
import json
import discord
import aiofiles
from PIL import Image


async def command(self, ctx, *args):
    if len(args) == 0:
        await ctx.send("you need to enter a group name.")
        return
    else:
        animename = args[0].capitalize()
        for arg in args[1:]:
            animename += " " + arg.capitalize()
    async with ClientSession() as session:
        async with session.get(
            f"{DB_BASE_ADDRESS}/weekly/{ctx.author.id}/{animename}"
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
                embed = discord.Embed(title="Weekly", color=0xFF00FF)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar
                )

                for key, value in card1.items():
                    if key != "url":
                        embed.add_field(name=f"Card1-{key}", value=value)
                for key, value in card2.items():
                    if key != "url":
                        embed.add_field(name=f"Card2-{key}", value=value)
                coinsGot = random.randint(12, 16)
                embed.add_field(name="Coins", value=f"{coinsGot}{EMOJIS_COIN}")

                embed.set_image(url=f"attachment://card.png")
                card1uid = card1["ID"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card1uid}/1"
                ) as r:
                    await r.text()
                card2uid = card2["ID"]
                async with session.get(
                    f"{DB_BASE_ADDRESS}/addcard/{ctx.author.id}/{card2uid}/1"
                ) as r:
                    await r.text()
                async with session.get(
                    f"{DB_BASE_ADDRESS}/changebalance/{ctx.author.id}/{coinsGot}"
                ) as r2:
                    await r2.text()
                await ctx.send(file=file, embed=embed)


def merge_images(image_list):
    images = [Image.open(x) for x in image_list]
    widths, heights = zip(*(i.size for i in images))
    spacing = 16
    total_width = sum(widths) + (len(images) - 1) * spacing
    max_height = max(heights)
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0] + spacing
    filepath = get_tempfilename()
    new_im.save(filepath)
    return filepath
