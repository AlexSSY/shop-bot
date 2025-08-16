from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import crud
import shared


router = Router(name='add_product_router')


class AddProductStates(StatesGroup):
    name = State()
    image_id = State()
    price = State()


@router.message(Command("add"))
async def add_new_item(message: Message, state: FSMContext):
    await state.set_state(AddProductStates.name)
    await message.answer("Enter item's name")


@router.message(AddProductStates.name)
async def process_add_product_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(AddProductStates.image_id)
    await message.answer("Send to me item's image")


@router.message(AddProductStates.image_id)
async def process_add_product_image(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image_id=image_id)
    await state.set_state(AddProductStates.price)
    await message.answer("Send to me item's price")


@router.message(AddProductStates.price)
async def process_add_product_price(message: Message, state: FSMContext):
    price = float(message.text)
    await state.update_data(price=price)
    item_data = await state.get_data()
    product_id = await crud.add_product(**item_data)
    await message.answer("Product successfully added in to shop.")
    await state.clear()
    product = await crud.get_product_by_id(product_id)
    product_text = await shared.get_product_detail_text(product)
    product_keyboard = await shared.get_product_detail_keyboard(product)
    await message.answer_photo(photo=product.image_id, caption=product_text, reply_markup=product_keyboard)
