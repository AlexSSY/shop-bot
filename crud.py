import aiosqlite


async def init_db(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_url TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        await db.commit()


# CREATE
async def add_product(db_path: str, name: str, image_url: str, price: float):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "INSERT INTO products (name, image_url, price) VALUES (?, ?, ?)",
            (name, image_url, price)
        )
        await db.commit()