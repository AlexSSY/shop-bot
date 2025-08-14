from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

import crud
import assets
from products import get_products_navigation_keyboard


router = Router(name='delete_product')


@router.callback_query(F.data.startswith('delete_'))
async def delete_product_handler(callback: CallbackQuery):
    _, page_str, product_id_str = callback.data.split("_", 2)
    product_id = int(product_id_str)
    page = int(page_str)
    delete_item_buttons = [
        [InlineKeyboardButton(text='Удалить', callback_data=f'confirm-delete_{page}_{product_id}')],
        [InlineKeyboardButton(text="Отмена", callback_data=f'detail_{page}_{product_id}')]
    ]
    delete_item_keyboard = InlineKeyboardMarkup(inline_keyboard=delete_item_buttons)
    await callback.message.edit_reply_markup(reply_markup=delete_item_keyboard)


@router.callback_query(F.data.startswith('confirm-delete_'))
async def delete_product_delete_confirm_handler(callback: CallbackQuery):
    _, page_str, product_id_str = callback.data.split("_", 2)
    product_id = int(product_id_str)
    page = int(page_str)
    
    await crud.delete_product(product_id)

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