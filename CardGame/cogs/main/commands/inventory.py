from aiohttp import ClientSession
from utilities.constants import *
from utilities.functions import *
from datetime import datetime, timezone
import discord
import asyncio


async def command(self, ctx, *args):
    async with ClientSession(trust_env=True) as session:
        useridforrequest = ctx.author.id
        if len(args) == 1 and get_input_type(args[0]) == Inputs.User:
            useridforrequest = get_user(args[0])
        current_page = 1
        params = {"page_size": str(INVENTORY_PAGE_SIZE), "page": current_page}
        async with session.get(
            f"{DB_BASE_ADDRESS}/inventory/{useridforrequest}", params=params
        ) as r:
            result = await r.json()
            page = 1
            cards = result["results"]
            count = result["count"]
            next = result["next"]
            prev = result["previous"]
            embed = discord.Embed(
                title=get_title(page, INVENTORY_PAGE_SIZE, count), color=0xFFFF00
            )
            embdisc = ""
            for card in cards:
                embdisc += card + "\n"
            embed.description = embdisc
            msg: discord.Message = await ctx.send(embed=embed)
            starttime = datetime.now(timezone.utc)
        for reaction in [EMOJIS_SKIPLEFT, EMOJIS_SKIP]:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            return (
                reaction.message.id == msg.id
                and user == ctx.author
                and str(reaction.emoji) in [EMOJIS_SKIPLEFT, EMOJIS_SKIP]
            )

        delay = 0
        while (
            datetime.now(timezone.utc) - starttime
        ).seconds < LONG_COMMAND_TIMEOUT + delay:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=5, check=check
                )
            except asyncio.TimeoutError:
                a = 1
            else:
                if next != None and str(reaction.emoji) == EMOJIS_SKIP:
                    current_page += 1
                    params = {
                        "page_size": str(INVENTORY_PAGE_SIZE),
                        "page": current_page,
                    }
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/inventory/{useridforrequest}", params=params
                    ) as r:
                        result = await r.json()
                        page = page + 1
                        cards = result["results"]
                        count = result["count"]
                        next = result["next"]
                        prev = result["previous"]
                        embed = discord.Embed(
                            title=get_title(page, INVENTORY_PAGE_SIZE, count),
                            color=0xFFFF00,
                        )
                        embdisc = ""
                        for card in cards:
                            embdisc += card + "\n"
                        embed.description = embdisc
                        await reaction.remove(ctx.author)
                        await msg.edit(embed=embed)
                        delay = min(LONG_COMMAND_TIMEOUT, delay + 5)
                elif prev != None and str(reaction.emoji) == EMOJIS_SKIPLEFT:
                    current_page -= 1
                    params = {
                        "page_size": str(INVENTORY_PAGE_SIZE),
                        "page": current_page,
                    }
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/inventory/{useridforrequest}", params=params
                    ) as r:
                        result = await r.json()
                        page = page - 1
                        cards = result["results"]
                        count = result["count"]
                        next = result["next"]
                        prev = result["previous"]
                        embed = discord.Embed(
                            title=get_title(page, INVENTORY_PAGE_SIZE, count),
                            color=0xFFFF00,
                        )
                        embdisc = ""
                        for card in cards:
                            embdisc += card + "\n"
                        embed.description = embdisc
                        await reaction.remove(ctx.author)
                        await msg.edit(embed=embed)
                        delay = min(LONG_COMMAND_TIMEOUT, delay + 5)
                else:
                    await reaction.remove(ctx.author)


def get_title(page, perpage, count):
    firstindex = (page - 1) * perpage + 1
    lastindex = firstindex + perpage - 1
    lastindex = min(lastindex, count)
    return f"Inventory {firstindex}-{lastindex} from {count} cards"
