import configparser
import enum
from os import path
import os
import re
import json
import uuid
import discord
import aiofiles
import importlib
from datas import common_emojis
from utilities.constants import *
from datetime import timedelta
from aiohttp import ClientSession
from PIL import Image


def parse_time(s) -> timedelta:
    if "day" in s:
        m = re.match(
            r"(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)",
            s,
        )
        d = m.groupdict()
        return timedelta(
            days=float(d["days"]),
            hours=float(d["hours"]),
            minutes=float(d["minutes"]),
            seconds=float(d["seconds"]),
        )
    else:
        m = re.match(r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)", s)
        d = m.groupdict()
        return timedelta(
            hours=float(d["hours"]),
            minutes=float(d["minutes"]),
            seconds=float(d["seconds"]),
        )


def get_cooldown(t):
    time = parse_time(t)
    if time < timedelta(seconds=0):
        return common_emojis.get_emoji(EMOJIS_COOLDOWN_CHECK)
    else:
        cooldown = ""
        if time.days > 0:
            cooldown += f"**{time.days}**Days, "
        if time.seconds // 3600 > 0:
            cooldown += f"**{time.seconds//3600}**hours "
        if int(time.seconds % 3600 // 60) > 0 or int(time.seconds / 360) > 0:
            cooldown += f"**{time.seconds%3600//60}**minutes "
        cooldown += f"**{time.seconds%60}**seconds"
        return cooldown


async def show_card(ctx, card, reactions, embedtitle, embedcolor):
    cardinfo: dict = json.loads(card)
    embed = discord.Embed(title=embedtitle, color=embedcolor)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    embed.description = cardinfo["CardDescription"]
    filepath = await get_image(cardinfo["url"])
    file = discord.File(filepath, filename="card.png")
    embed.set_image(url="attachment://card.png")
    msg: discord.Message = await ctx.send(file=file, embed=embed)
    for reaction in reactions:
        await msg.add_reaction(reaction)
    return cardinfo, embed, msg


def add_duplicate_to_embed(duplicate, embed):
    if duplicate == "True":
        emoji = common_emojis.get_emoji("GENERIC_DUPLICATE")
        embed.description += f"\n> \n> {emoji} **Duplicate**"
    else:
        emoji = common_emojis.get_emoji("GENERIC_NEWCARD")
        embed.description += f"\n > \n> {emoji} **New Card!**"


async def get_card_embed(ctx, card, embedtitle, embedcolor):
    cardinfo = json.loads(card)
    embed = discord.Embed(title=embedtitle, color=embedcolor)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    embed.description = cardinfo["CardDescription"]
    filepath = await get_image(cardinfo["url"])
    file = discord.File(filepath, filename="card.png")
    embed.set_image(url="attachment://card.png")
    return cardinfo, embed, file


async def check_can_claim(self, user, ctx) -> bool:
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/cds/{user.id}") as r:
            if r.status == 404:
                await ctx.send(f'{user.mention} register with "start" first.')
                return False
            else:
                items = json.loads(await r.text())
                cd = items["Claim"]
                deltatime = parse_time(cd)
                if deltatime > timedelta(seconds=0):
                    await ctx.send(
                        f"{user.mention} Wait for {get_cooldown(cd)} before another claim."
                    )
                    return False
                else:
                    async with ClientSession() as session:
                        async with session.get(
                            f"{DB_BASE_ADDRESS}/claim/{user.id}"
                        ) as r:
                            await r.text()
                    return True


def get_input_type(input: str):
    if (
        (input.startswith("<@") or input.startswith("<@!"))
        and input.endswith(">")
        and len(input) > 19
        and len(input) < 23
    ):
        return Inputs.User
    if input.isdigit() and len(input) > 16 and len(input) < 19:
        return Inputs.User
    if input.isdigit():
        return Inputs.Number
    if len(input) > 6 and input[-1:].isdigit():
        return Inputs.Card
    return Inputs.Invalid


class Inputs(enum.Enum):
    User = 1
    Card = 2
    Number = 3
    Invalid = 4


def get_user(input: str):
    return input.strip("<").strip(">").strip("@").strip("!")


def get_card(input):
    return str(input).upper()


def get_tempfilename():
    filename = path.join(TEMP_FILE_ADDRESS, f"{uuid.uuid4()}.png")
    while path.exists(filename):
        filename = path.join(TEMP_FILE_ADDRESS, f"{uuid.uuid4()}.png")
    return filename


async def get_image(url):
    if LOCAL_MEDIA_FILES:
        filename = path.join(LOCAL_MEDIA_ADDRESS, url[1:])
    else:
        address = REMOTE_MEDIA_ADDRESS + url
        async with ClientSession() as session:
            async with session.get(address) as r:
                filename = get_tempfilename()
                async with aiofiles.open(filename, mode="wb") as f1:
                    await f1.write(await r.read())
                    await f1.close()
    return filename


def read_config(section, key):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE_ADDRESS)
    return parser.get(section, key)


def get_databaseconfigs_dir():
    return os.path.join(BASE_DIR, "datas")


def get_cogs_dir():
    return os.path.join(BASE_DIR, "cogs")


async def load_cogs(bot):
    cog_folders = [f for f in os.scandir(get_cogs_dir()) if f.is_dir()]
    for cog_folder in cog_folders:
        for file in os.listdir(cog_folder.path):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{cog_folder.name}.{file[:-3]}")


async def load_database_datas():
    files = [f for f in os.scandir(get_databaseconfigs_dir()) if f.name.endswith(".py")]
    for file in files:
        mod = importlib.import_module(f"datas.{file.name[:-3]}")
        if mod != None:
            func = getattr(mod, "load", None)
            if func != None:
                await func()


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