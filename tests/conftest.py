import glob
import discord
import discord.ext.commands as commands
import os
import pytest_asyncio
import discord.ext.test as dpytest

@pytest_asyncio.fixture
async def bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=">", intents=intents)
    print(os.getcwd())
    await bot._async_setup_hook()
    dpytest.configure(bot)
    cog_folders = [f for f in os.scandir("./cogs") if f.is_dir()]
    for cog_folder in cog_folders:
        for file in os.listdir(cog_folder.path):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{cog_folder.name}.{file[:-3]}")
    return bot

@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()

def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob('./dpytest_*.dat')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)