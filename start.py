import discord
import os
from discord.ext import commands, tasks
import asyncio
from utilities.constants import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    update_status.start()


@tasks.loop(minutes=10)
async def update_status():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"Shuffling in {len(bot.guilds)} servers"),
    )


cog_folders = [f for f in os.scandir("./cogs") if f.is_dir()]
for cog_folder in cog_folders:
    for file in os.listdir(cog_folder.path):
        if file.endswith(".py"):
            asyncio.run(bot.load_extension(f"cogs.{cog_folder.name}.{file[:-3]}"))


bot.run(BOT_TOKEN)
