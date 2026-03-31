from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_kb import main_kb
from texts import START_TEXT

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(START_TEXT, reply_markup=main_kb)
