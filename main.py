import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import settings
import add_product
import products
import delete_product


dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello from aiogram bot.")


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp.include_router(add_product.router)
    dp.include_router(products.router)
    dp.include_router(delete_product.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
