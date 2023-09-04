from aiohttp.client import ClientSession

from utilities.constants import *

dictionary = {}


def get_emoji(label):
    if label in dictionary:
        return dictionary[label]
    return ""


async def load():
    async with ClientSession() as session:
        async with session.get(f"{DB_CONFIGS_ADDRESS}/commonemojis") as r:
            if r.status == 200:
                dictionary.clear()
                content = await r.json()
                for emoji in content:
                    dictionary[emoji["name"]] = emoji["emoji"]
                print(f"loaded {len(dictionary)} items.")
            else:
                print(r._traces)
