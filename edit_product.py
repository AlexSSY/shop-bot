from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import crud


router = Router(name='edit_product_router')


class EditProductStates(StatesGroup):
    product_id = State()
    name = State()
    image_id = State()
    price = State()


@router.callback_query(F.data.startswith('edit_'))
async def add_new_item(query: CallbackQuery, state: FSMContext):
    await state.set_state(EditProductStates.name)
    _, id_str = query.data.split('_')
    id = int(id_str)
    await state.update_data(product_id=id)
    await query.message.answer("Enter new item's name")


@router.message(EditProductStates.name)
async def process_add_product_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(EditProductStates.image_id)
    await message.answer("Send to me new item's image")


@router.message(EditProductStates.image_id)
async def process_add_product_image(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image_id=image_id)
    await state.set_state(EditProductStates.price)
    await message.answer("Send to me new item's price")


@router.message(EditProductStates.price)
async def process_add_product_price(message: Message, state: FSMContext):
    price = float(message.text)
    await state.update_data(price=price)
    item_data = await state.get_data()
    await crud.update_product(**item_data)
    await message.answer("Product successfully updated.")
    await state.clear()
