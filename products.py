from aiogram import Router
import math
from typing import Optional

from aiogram import F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
)
from aiogram.filters import Command

import crud
import assets
import shared


router = Router(name='products')


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
        [InlineKeyboardButton(text=p.name, callback_data=f"detail_{page}_{p.id}")]
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


@router.message(Command("products"))
async def products_command_handler(message: Message):
    keyboard = await get_products_navigation_keyboard(1)
    if keyboard is None:
        await message.answer("You do not have any products in your shop.")
        return
    
    await message.answer_photo(
        photo=assets.background_image,
        caption='Select your item from list below',
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("detail_"))
async def product_detail_handler(callback: CallbackQuery):
    _, page_str, product_id_str = callback.data.split("_", 2)
    product_id = int(product_id_str)
    page = int(page_str)
    product = await crud.get_product_by_id(product_id)

    if product is not None:
        product_detail_text = await shared.get_product_detail_text(product)
        back_kb = await shared.get_product_detail_keyboard(product, page)
        # Отправляем фото с подписью
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=product.image_id,
                caption=product_detail_text
            ),
            reply_markup=back_kb,
        )
        await callback.answer()  # Убираем "часики"
    else:
        await callback.answer(
            f"Product with id: {product_id} is not exists anymore.", show_alert=True
        )


# Обработчик кнопки "Назад"
@router.callback_query(F.data == "back_to_list")
async def back_to_list_handler(callback: CallbackQuery):
    keyboard = await get_products_navigation_keyboard(1)
    if keyboard is None:
        await callback.message.answer("You do not have any products in your shop.")
        return
    await callback.message.answer('Select your item from list below', reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("page_"))
async def products_page_handler(callback: CallbackQuery):
    # Извлекаем номер страницы
    page = int(callback.data.split("_")[1])

    # Получаем клавиатуру для новой страницы
    keyboard = await get_products_navigation_keyboard(page)

    # Если у тебя сообщение с текстом (без фото):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=assets.background_image,
            caption="Select your item from list below"
        ),
        reply_markup=keyboard
    )

    await callback.answer()
