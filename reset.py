'''
Re-create DB and seed
'''

import asyncio

import create
import drop
import seed


async def reset_db():
    await drop.drop_db()
    await create.create_db()
    await seed.seed()


if __name__ == '__main__':
    asyncio.run(reset_db())
