import aiosqlite

import settings


async def init_db():
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_url TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        await db.commit()


async def add_product(name: str, image_url: str, price: float):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute(
            "INSERT INTO products (name, image_url, price) VALUES (?, ?, ?)",
            (name, image_url, price)
        )
        await db.commit()


async def get_all_products():
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        async with db.execute("SELECT id, name, image_url, price FROM products") as cursor:
            return await cursor.fetchall()


async def get_product_by_id(product_id: int):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        async with db.execute(
            "SELECT id, name, image_url, price FROM products WHERE id = ?",
            (product_id,)
        ) as cursor:
            return await cursor.fetchone()
        

async def update_product(product_id: int, name: str, image_url: str, price: float):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute(
            "UPDATE products SET name = ?, image_url = ?, price = ? WHERE id = ?",
            (name, image_url, price, product_id)
        )
        await db.commit()


async def delete_product(product_id: int):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()
