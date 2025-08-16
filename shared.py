from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_product_detail_text(product):
    return f"Name: {product.name}\n\nPrice: {product.price}$"


async def get_product_detail_keyboard(product, page = 1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_{product.id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{page}_{product.id}")],
            [InlineKeyboardButton(text="⬅️ Венрнуться к списку", callback_data=f"page_{page}")],
        ]
    )
