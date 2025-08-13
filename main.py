import math
import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
)
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


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello from aiogram bot.")


@dp.message(Command("add"))
async def add_new_item(message: Message, state: FSMContext):
    await state.set_state(AddProductStates.name)
    await message.answer("Enter item's name")


async def get_products_navigation_keyboard(page: int, per_page: int = 5) -> Optional[InlineKeyboardMarkup]:
    products_count = await crud.get_products_count()

    if products_count == 0:
        return None

    max_pages = math.ceil(products_count / per_page)
    page = max(1, min(page, max_pages))  # ограничиваем диапазон

    limit = per_page
    offset = (page - 1) * per_page

    products = await crud.get_all_products(limit, offset)

    buttons = [
        [InlineKeyboardButton(text=p.name, callback_data=f"detail_{p.id}")]
        for p in products
    ]

    # Кнопки навигации
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))
    if page < max_pages:
        nav_buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"page_{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(Command("products"))
async def products_command_handler(message: Message):
    keyboard = await get_products_navigation_keyboard(1)
    if keyboard is None:
        await message.answer("You do not have any products in your shop.")
        return
    await message.answer('Select your item from list below', reply_markup=keyboard)


@dp.callback_query(F.data.startswith("detail_"))
async def product_detail_handler(callback: CallbackQuery):
    product_id = callback.data.split("_", 1)[1]  # Берём только ID
    product = await crud.get_product_by_id(product_id)

    if product is not None:
        back_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_{product_id}")],
                [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{product_id}")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_list")],
            ]
        )
        # Отправляем фото с подписью
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=product.image_url,
                caption=f"Name: {product.name}\n\nPrice: {product.price}$"
            ),
            reply_markup=back_kb,
        )
        await callback.answer()  # Убираем "часики"
    else:
        await callback.answer(
            f"Product with id: {product_id} is not exists anymore.", show_alert=True
        )


# Обработчик кнопки "Назад"
@dp.callback_query(F.data == "back_to_list")
async def back_to_list_handler(callback: CallbackQuery):
    keyboard = await get_products_navigation_keyboard(1)
    if keyboard is None:
        await callback.message.answer("You do not have any products in your shop.")
        return
    await callback.message.answer('Select your item from list below', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(F.data.startswith("page_"))
async def products_page_handler(callback: CallbackQuery):
    # Извлекаем номер страницы
    page = int(callback.data.split("_")[1])

    # Получаем клавиатуру для новой страницы
    keyboard = await get_products_navigation_keyboard(page)

    # Если у тебя сообщение с текстом (без фото):
    await callback.message.edit_text(
        text="Select your item from list below",
        reply_markup=keyboard
    )

    await callback.answer()


@dp.message(AddProductStates.name)
async def process_add_product_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(AddProductStates.image_url)
    await message.answer("Send to me item's image")


@dp.message(AddProductStates.image_url)
async def process_add_product_image(message: Message, state: FSMContext):
    image_url = message.photo[-1].file_id
    await state.update_data(image_url=image_url)
    await state.set_state(AddProductStates.price)
    await message.answer("Send to me item's price")


@dp.message(AddProductStates.price)
async def process_add_product_price(message: Message, state: FSMContext):
    price = float(message.text)
    await state.update_data(price=price)
    item_data = await state.get_data()
    await crud.add_product(**item_data)
    await message.answer("Product successfully added in to shop.")
    await state.clear()


async def main():
    await crud.init_db()

    bot = Bot(settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
