'''
Drop DB
'''

import aiosqlite
import asyncio

import settings


async def drop_db():
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute("DROP TABLE IF EXISTS products")
        await db.commit()


if __name__ == '__main__':
    asyncio.run(drop_db())
