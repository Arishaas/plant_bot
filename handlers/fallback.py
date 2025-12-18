from aiogram import Router
from aiogram.types import Message
from texts import UNKNOWN_COMMAND

router = Router()


@router.message()
async def unknown(message: Message):
    await message.answer(UNKNOWN_COMMAND)
