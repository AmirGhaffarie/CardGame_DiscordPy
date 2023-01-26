import discord.ext.commands as commands
import os
import asyncio
import pytest
import pytest_asyncio
import discord.ext.test as dpytest


@pytest.mark.asyncio
async def test_bot_startup(bot):
    await dpytest.message(">t")
    assert dpytest.verify().message().contains().content("Ping:")