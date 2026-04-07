from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import get_user_plants
from keyboards.main_kb import main_kb

router = Router()


@router.message(lambda m: m.text == "🌺 Мои растения")
async def list_plants(message: Message):
    plants = await get_user_plants(message.from_user.id)
    if not plants:
        return await message.answer("🌱 У вас пока нет растений")
    text = "🌺 Ваши растения:\n\n"
    for i, plant in enumerate(plants, start=1):
        text += f"{i}. {plant[0]}\n"
    await message.answer(text)


@router.message(lambda m: m.text == "❌🗑 Удаление растения")
async def delete_prompt(message: Message):
    await message.answer("❌ Введите название растения для удаления")
