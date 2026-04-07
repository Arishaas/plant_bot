from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from plant_states import DeletePlant
from database import get_user_plant, delete_plant

router = Router()


@router.message(lambda m: m.text and "Удалить" in m.text)
async def delete_plant_start(message: Message, state: FSMContext):
    await message.answer("🗑 Введите название растения, которое хотите удалить")
    await state.set_state(DeletePlant.waiting_for_name)


@router.message(DeletePlant.waiting_for_name)
async def delete_plant_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("❌ Растение не найдено")

    await delete_plant(message.from_user.id, name)

    await message.answer(f"🗑 Растение удалено: {name}")
    await state.clear()
