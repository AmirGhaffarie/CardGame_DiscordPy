from datas import emojis, localization


async def command(self, ctx):
    await emojis.load()
    await localization.load()
    await ctx.send("Reload Completed")
