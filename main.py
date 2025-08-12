import os
import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv


CURRENT_PATH = Path(__file__).resolve().parent


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv("DB_NAME")

DB_FILE_PATH = CURRENT_PATH / DB_NAME


dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello from aiogram bot.')


async def main():
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
