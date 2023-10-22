from discord.ext import commands

from cogs.main.commands import *


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        await start_command(self, ctx)

    @commands.command(aliases=["ccd", "CCD"])
    async def cardcooldown(self, ctx):
        await ccd_command(self, ctx)

    @commands.command(aliases=["scd", "SCD"])
    async def starcooldown(self, ctx):
        await scd_command(self, ctx)

    @commands.command(aliases=["cd", "CD"])
    async def cooldown(self, ctx):
        await cd_command(self, ctx)

    @commands.command(aliases=["d", "D"])
    async def drop(self, ctx):
        await drop_command(self, ctx)

    @commands.command(aliases=["sg", "SG", "Sg"])
    async def stargaze(self, ctx):
        await stargaze_command(self, ctx)

    @commands.command(aliases=["di", "DI", "Di"])
    async def discover(self, ctx):
        await discover_command(self, ctx)

    @commands.command(aliases=["l", "L"])
    async def lucky(self, ctx):
        await lucky_command(self, ctx)

    @commands.command(aliases=["l2", "L2"])
    async def lucky2(self, ctx):
        await lucky2_command(self, ctx)

    @commands.command(aliases=["i", "I", "inv"])
    async def inventory(self, ctx, *args):
        await inventory_command(self, ctx, *args)

    @commands.command(aliases=["v", "V", "vW", "Wv", "VW", "vw"])
    async def view(self, ctx, *args):
        await view_command(self, ctx, *args)

    @commands.command(aliases=["g", "G"])
    async def gift(self, ctx, *args):
        await gift_command(self, ctx, *args)

    @commands.command()
    async def daily(self, ctx, *args):
        await daily_command(self, ctx, *args)

    @commands.command(aliases=["b", "B", "$"])
    async def balance(self, ctx, *args):
        await balance_command(self, ctx, *args)

    @commands.command(aliases=["w", "W"])
    async def weekly(self, ctx, *args):
        await weekly_command(self, ctx, *args)

    @commands.command(aliases=["r", "R"])
    async def reload(self, ctx, *args):
        await reload_command(self, ctx, *args)

    @commands.command(aliases=["h", "H", "abrazo"])
    async def hug(self, ctx, *args):
        await hug_command(self, ctx, *args)

    @commands.command()
    async def kiss(self, ctx, *args):
        await kiss_command(self, ctx, *args)

    @commands.command()
    async def happy(self, ctx, *args):
        await happy_command(self, ctx, *args)

    @commands.command()
    async def run(self, ctx, *args):
        await run_command(self, ctx, *args)

    @commands.command()
    async def sip(self, ctx, *args):
        await sip_command(self, ctx, *args)

    @commands.command()
    async def wave(self, ctx, *args):
        await wave_command(self, ctx, *args)

    @commands.command()
    async def nod(self, ctx, *args):
        await nod_command(self, ctx, *args)


async def setup(client):
    await client.add_cog(Main(client))
