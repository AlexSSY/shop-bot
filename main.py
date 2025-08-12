import os
import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import crud
import settings


dp = Dispatcher(storage=MemoryStorage())


class AddProductStates(StatesGroup):
    name = State()
    image_url = State()
    price = State()


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello from aiogram bot.')


@dp.message(Command('add'))
async def add_new_item(message: Message, fsm: FSMContext):
    await fsm.set_state(AddProductStates.name)
    await message.answer("Enter item's name")


@dp.message(AddProductStates.name)
async def process_add_product_name(message: Message, fsm: FSMContext):
    name = message.text.strip()
    await fsm.update_data(name=name)
    await fsm.set_state(AddProductStates.image_url)
    await message.answer("Send to me item's image")


@dp.message(AddProductStates.image_url)
async def process_add_product_image(message: Message, fsm: FSMContext):
    image_url = message.photo[-1].file_id
    await fsm.update_data(image_url=image_url)
    await fsm.set_state(AddProductStates.price)
    await message.answer("Send to me item's price")


@dp.message(AddProductStates.price)
async def process_add_product_price(message: Message, fsm: FSMContext):
    price = float(message.text)
    await fsm.update_data(price=price)
    item_data = await fsm.get_data()
    await crud.add_product(**item_data)
    await message.answer('Product successfully added in to shop.')
    await fsm.clear()


async def main():
    await crud.init_db()

    bot = Bot(settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
