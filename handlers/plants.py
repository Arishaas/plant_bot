from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from database import add_user_plant, get_user_plants

router = Router()


@router.message(Command("addplant"))
async def addplant(message: Message, command: CommandObject):
    name = (command.args or "").strip().lower()

    if not name:
        return await message.answer("Использование: /addplant <название>")

    await add_user_plant(message.from_user.id, name)
    await message.answer(f"Добавлено: {name}")


@router.message(Command("myplants"))
async def myplants(message: Message):
    plants = await get_user_plants(message.from_user.id)

    if not plants:
        return await message.answer("У вас еще нет растений. Добавьте через /addplant")

    text = "Ваши растения:\n\n"
    for name, lw, lf, lt, notes in plants:
        text += (
            f"{name}\n"
            f"Полив: {lw}\n"
            f"Подкормка: {lf}\n"
            f"Пересадка: {lt}\n"
        )
        if notes:
            text += f"Заметка: {notes}\n"
        text += "\n"

    await message.answer(text)
