from datas import emojis, localization, embeds, discoveries


async def command(self, ctx):
    await embeds.load()
    await emojis.load()
    await localization.load()
    await discoveries.load()
    await ctx.send("Reload Completed")
