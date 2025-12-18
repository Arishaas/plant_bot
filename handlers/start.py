from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database import add_user
from texts import START_TEXT

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer(START_TEXT)
