'''
Create DB
'''

import aiosqlite

import settings


async def create_db():
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_id TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        await db.commit()
