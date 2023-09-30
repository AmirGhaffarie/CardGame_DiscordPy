from aiohttp.client import ClientSession

from utilities.constants import *
from utilities.functions import fill_embed_desc
dictionary = {}


def get(label, content_dict):
    if label in dictionary:
        return fill_embed_desc(dictionary[label], content_dict)
    return "embed not found"


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
