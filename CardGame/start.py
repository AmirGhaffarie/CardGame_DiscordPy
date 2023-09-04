import asyncio

import discord
from discord.ext import commands, tasks

from utilities.functions import read_config, load_cogs, load_database_datas

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
        activity=discord.Game(f"in {len(bot.guilds)} servers"),
    )


asyncio.run(load_cogs(bot))

asyncio.run(load_database_datas())

bot.run(read_config("Bot", "Token"))
