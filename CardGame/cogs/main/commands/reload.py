from CardGame.datas import common_emojis, localization


async def command(self, ctx):
    await common_emojis.load()
    await localization.load()
    await ctx.send("Reload Completed")
