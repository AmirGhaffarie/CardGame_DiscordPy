from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from aiohttp.client import ClientSession
from datetime import datetime
import discord
from utilities.constants import *
from utilities.functions import get_file, load_from_url, get_tempfilename


async def command(self, ctx, *args):
    async with ClientSession() as session:
        async with session.get(f"{DB_BASE_ADDRESS}/register/{ctx.author.id}") as r:
            if r.status == 210 or len(args) > 0:
                await show_card(ctx)
            else:
                await ctx.send(await r.text())


async def show_card(ctx):
    img_address = await make_image(ctx)
    file = discord.File(img_address, filename="card.png")
    embed = discord.Embed(title="Register", color=0x9CB6EB, url="attachment://card.png")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    await ctx.send(file=file, embed=embed)


async def make_image(ctx):
    img_back = Image.open(await get_file("/media/custom/start_card_back.png"))

    member: discord.Member = ctx.author
    pfp = Image.open(await load_from_url(member.avatar.url))

    pfp = pfp.resize((530, 530))

    result = Image.new("RGBA", img_back.size)
    result.paste(pfp, (950, 225))
    result.paste(img_back, mask=img_back)

    draw = ImageDraw.Draw(result)

    font = ImageFont.truetype(await get_file("/media/custom/bot_font.otf"), 53)

    date = datetime.now()

    pos = [270, 430, 585]
    text = [f"@{member.name}", member.name if member.nick is None else member.nick, date.strftime("%m/%d/%y")]
    fill = (93, 145, 255)
    outline = (255, 255, 255)

    for i in range(3):
        draw.text((40, pos[i]), text[i], font=font, fill=fill, stroke_fill=outline, stroke_width=3, align="left")

    filename = get_tempfilename()
    result.save(filename)
    return filename
