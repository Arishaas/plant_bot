from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from plant_states import AddPlant
from database import add_user_plant

router = Router()


@router.message(lambda m: m.text and "➕ Добавить растение" in m.text)
async def add_start(message: Message, state: FSMContext):
    await message.answer("🌱 Введите название растения")
    await state.set_state(AddPlant.waiting_for_name)


@router.message(AddPlant.waiting_for_name)
async def add_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()

    await add_user_plant(message.from_user.id, name)

    await message.answer(f"➕🌺 Добавлено растение {name}")
    await state.clear()
