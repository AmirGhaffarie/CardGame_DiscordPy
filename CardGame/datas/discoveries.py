import random

from aiohttp.client import ClientSession

from utilities.constants import *
items = []
weights = []


def get() -> (int, str):
    item = random.choices(items, weights=weights, k=1)[0]
    return item["amount"], item["description"]


async def load():
    async with ClientSession() as session:
        async with session.get(f"{DB_CONFIGS_ADDRESS}/discover") as r:
            if r.status == 200:
                items.clear()
                weights.clear()
                content = await r.json()
                for item in content:
                    items.append(item)
                    weights.append(item["chance"])
                print(f"loaded {len(items)} items.")
            else:
                print(r._traces)
