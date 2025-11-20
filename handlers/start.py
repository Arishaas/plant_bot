from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🌿 Привет! Я бот, который поможет ухаживать за растениями.\n\n"
        "Добавить растение: /addplant <название>\n"
        "Ваши растения: /myplants\n"
        "Дата полива: /water <растение>\n"
        "Дата подкормки: /feed <растение> [дата]\n"
        "Дата пересадки: /transplant <растение> [дата]\n"
        "Статус: /status <растение>\n"
        "Заметка: /note <растение> <текст>"
    )
