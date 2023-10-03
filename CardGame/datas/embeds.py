from aiohttp.client import ClientSession
import re

from datas import emojis
from utilities.constants import *
dictionary = {}


def get(label, content_dict):
    if label in dictionary:
        return fill_embed_desc(dictionary[label], content_dict)
    return "embed not found"


def fill_embed_desc(embed, variables) -> str:
    return re.sub("<(.*?)>", lambda x: (check_embed_var(x, variables)), embed)


def check_embed_var(var: re.Match, variables) -> str:
    match_string = var.group()[1:-1]
    if match_string.startswith("e:"):
        return emojis.get(match_string[2:].upper())
    return variables[match_string]


async def load():
    async with ClientSession() as session:
        async with session.get(f"{DB_CONFIGS_ADDRESS}/embeds") as r:
            if r.status == 200:
                dictionary.clear()
                content = await r.json()
                for embed in content:
                    dictionary[embed["name"]] = embed["embed"]
                print(f"loaded {len(dictionary)} items.")
            else:
                print(r._traces)
