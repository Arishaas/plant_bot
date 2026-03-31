from aiogram import Router
from aiogram.types import Message
from database import get_user_plants

router = Router()


@router.message(lambda m: m.text == "🌺 Мои растения")
async def myplants(message: Message):
    plants = await get_user_plants(message.from_user.id)

    if not plants:
        return await message.answer("🌺 У вас нет растений")

    text = "🌺 Ваши растения:\n\n"
    for name, lw, lf, lt, notes in plants:
        text += f"{name}\n\n"

    await message.answer(text)
