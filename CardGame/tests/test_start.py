import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_bot_startup(bot):
    await dpytest.message(">t")
    assert dpytest.verify().message().contains().content("Ping:")
