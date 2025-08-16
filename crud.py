from typing import List, Optional
import aiosqlite

import settings
from models import Product


async def add_product(name: str, image_id: str, price: float) -> Optional[int]:
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO products (name, image_id, price) VALUES (?, ?, ?)",
            (name, image_id, price)
        )
        await db.commit()
        return cursor.lastrowid


async def get_products_count() -> int:
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM products") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_all_products(limit: int = 8, offset: int = 0) -> List[Product]:
    limit = max(1, int(limit))
    offset = max(0, int(offset))

    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        query = """
            SELECT id, name, image_id, price
            FROM products
            ORDER BY id
            LIMIT ? OFFSET ?
        """
        async with db.execute(query, (limit, offset)) as cursor:
            raw = await cursor.fetchall()
            return (Product(id=row[0], name=row[1], image_id=row[2], price=row[3]) for row in raw)


async def get_product_by_id(product_id: int) -> Optional[Product]:
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        async with db.execute(
            "SELECT id, name, image_id, price FROM products WHERE id = ?",
            (product_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return Product(*row)
        

async def update_product(product_id: int, name: str, image_id: str, price: float):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute(
            "UPDATE products SET name = ?, image_id = ?, price = ? WHERE id = ?",
            (name, image_id, price, product_id)
        )
        await db.commit()


async def delete_product(product_id: int):
    async with aiosqlite.connect(settings.DB_FILE_PATH) as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()
