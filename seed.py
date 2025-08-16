'''
Generate products in DB for testing
'''

import asyncio
import random

from faker import Faker

import crud


fake = Faker('en-us')


async def seed():
    for _ in range(25):
        await crud.add_product(
            name=fake.name_nonbinary(),
            image_id='AgACAgIAAxkBAAMhaJtOO4COGRLHm325QKha7bn9i8cAAkkDMhum1eBIOsMjyypju6gBAAMCAAN5AAM2BA',
            price=round(random.random(), 2)
        )


if __name__ == '__main__':
    asyncio.run(seed())
