from datas import emojis, localization, embeds


async def command(self, ctx):
    await embeds.load()
    await emojis.load()
    await localization.load()
    await ctx.send("Reload Completed")
