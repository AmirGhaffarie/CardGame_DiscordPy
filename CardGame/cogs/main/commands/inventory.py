import asyncio
from datetime import datetime, timezone

import discord

from utilities.functions import *


async def command(self, ctx, *args):
    async with ClientSession(trust_env=True) as session:
        user_id_for_request = ctx.author.id
        if len(args) >= 1 and get_input_type(args[0]) == Inputs.User:
            user_id_for_request = get_user(args[0])
        args_dict = get_args(args)
        current_page = 1
        params = {"page_size": str(INVENTORY_PAGE_SIZE), "page": current_page}
        params.update(args_dict)
        async with session.get(
            f"{DB_BASE_ADDRESS}/inventory/{user_id_for_request}", params=params
        ) as r:
            result = await r.json()
            page = 1
            cards = result["results"]
            count = result["count"]
            next = result["next"]
            prev = result["previous"]
            if count <= 0:
                await ctx.send("No card found with the filters")
                return
            embed = discord.Embed(
                title=get_title(page, INVENTORY_PAGE_SIZE, count), color=0x9CB6EB
            )
            next_emoji = emojis.get(EMOJIS_SKIP)
            prev_emoji = emojis.get(EMOJIS_SKIPLEFT)

            embed.description = get_cards_desc(cards)

            msg: discord.Message = await ctx.send(embed=embed)
            start_time = datetime.now(timezone.utc)
        for reaction in [prev_emoji, next_emoji]:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            return (
                reaction.message.id == msg.id
                and user == ctx.author
                and str(reaction.emoji) in [prev_emoji, next_emoji]
            )

        delay = 0
        while (
            datetime.now(timezone.utc) - start_time
        ).seconds < LONG_COMMAND_TIMEOUT + delay:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=5, check=check
                )
            except asyncio.TimeoutError:
                a = 1
            else:
                if next != None and str(reaction.emoji) == next_emoji:
                    current_page += 1
                    params = {
                        "page_size": str(INVENTORY_PAGE_SIZE),
                        "page": current_page,
                    }
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/inventory/{user_id_for_request}",
                        params=params,
                    ) as r:
                        result = await r.json()
                        page = page + 1
                        cards = result["results"]
                        count = result["count"]
                        next = result["next"]
                        prev = result["previous"]
                        embed = discord.Embed(
                            title=get_title(page, INVENTORY_PAGE_SIZE, count),
                            color=0x9CB6EB,
                        )
                        embed.description = get_cards_desc(cards)
                        await reaction.remove(ctx.author)
                        await msg.edit(embed=embed)
                        delay = min(LONG_COMMAND_TIMEOUT, delay + 5)
                elif prev != None and str(reaction.emoji) == prev_emoji:
                    current_page -= 1
                    params = {
                        "page_size": str(INVENTORY_PAGE_SIZE),
                        "page": current_page,
                    }
                    async with session.get(
                        f"{DB_BASE_ADDRESS}/inventory/{user_id_for_request}",
                        params=params,
                    ) as r:
                        result = await r.json()
                        page = page - 1
                        cards = result["results"]
                        count = result["count"]
                        next = result["next"]
                        prev = result["previous"]
                        embed = discord.Embed(
                            title=get_title(page, INVENTORY_PAGE_SIZE, count),
                            color=0x9CB6EB,
                        )
                        embed.description = get_cards_desc(cards)
                        await reaction.remove(ctx.author)
                        await msg.edit(embed=embed)
                        delay = min(LONG_COMMAND_TIMEOUT, delay + 5)
                else:
                    await reaction.remove(ctx.author)
        await msg.clear_reactions()


def get_args(*args):
    args_length = len(args)
    if args_length > 0:
        params = {}
        for index in range(args_length):
            if args[index] == "g" and index + 1 < args_length:
                params["group"] = args[index + 1]
            if args[index] == "e" and index + 1 < args_length:
                params["era"] = args[index + 1]
            if args[index] == "i" and index + 1 < args_length:
                params["idol"] = args[index + 1]
    else:
        return {}


def get_title(page, perpage, count):
    firstindex = (page - 1) * perpage + 1
    lastindex = firstindex + perpage - 1
    lastindex = min(lastindex, count)
    emoji = emojis.get("BACKPACK")
    return f"{emoji}Inventory\n**{firstindex}**->**{lastindex}** from **{count}**"


def get_cards_desc(cards):
    dict = {}
    for card in cards:
        lines = card.splitlines()
        gp = lines[0]
        era = lines[1]
        card = lines[2]
        if not gp in dict:
            dict[gp] = {}
        if not era in dict[gp]:
            dict[gp][era] = [card]
        else:
            dict[gp][era].append(card)
    result = ""
    arrow = emojis.get("GENERIC_RIGHTARROW")
    triangle = emojis.get("GENERIC_LINESTART")
    for group in dict:
        for era, card_list in dict[group].items():
            result += f"{arrow} **{group}**:\n"
            result += f"> {triangle} **{era}** • ({len(card_list)})\n"
            for card_info in card_list:
                result += card_info + "\n"
    return result
