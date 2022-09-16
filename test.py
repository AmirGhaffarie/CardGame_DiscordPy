import asyncio
from utilities.functions import getImage


image =  asyncio.run(getImage(''))
print(image)