from utilities.constants import *
from datas import common_emojis


async def command(self, ctx):
    await common_emojis.load()
    await ctx.send("Reload Completed")
