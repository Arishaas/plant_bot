from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils import pars_datetoken, days_until
from database import (
    get_user_plant, update_user_date, update_notes, get_plant_default
)

router = Router()


@router.message(Command("water"))
async def water(message: Message):
    name = message.get_args().lower().strip()
    if not name:
        return await message.answer("Использование: /water <название>")
    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")
    today = pars_datetoken("today")
    await update_user_date(message.from_user.id, name, "last_water", today)
    await message.answer(f"Полив обновлен {name} - {today}")


@router.message(Command("feed"))
async def feed(message: Message):
    args = message.get_args().split()
    if not args:
        return await message.answer("Использование: /feed <название> [дата]")

    name = args[0].lower()
    date_token = args[1] if len(args) > 1 else "today"
    date_iso = pars_datetoken(date_token)
    if not date_iso:
        return await message.answer("Неверная дата, формат YYYY-MM-DD или today")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    await update_user_date(message.from_user.id, name, "last_feed", date_iso)
    await message.answer(f"Дата подкормки обновлена {name} - {date_iso}")


@router.message(Command("transplant"))
async def transplant(message: Message):
    args = message.get_args().split()
    if not args:
        return await message.answer("Использование: /transplant <название> [дата]")

    name = args[0].lower()
    date_token = args[1] if len(args) > 1 else "today"
    date_iso = pars_datetoken(date_token)
    if not date_iso:
        return await message.answer("Неверная дата, формат YYYY-MM-DD или today")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    await update_user_date(message.from_user.id, name, "last_trans", date_iso)
    await message.answer(f"Дата пересадки обновлена {name} - {date_iso}")


@router.message(Command("status"))
async def status(message: Message):
    name = message.get_args().strip().lower()
    if not name:
        return await message.answer("Использование: /status <название>")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    name, lw, lf, lt, notes = row
    defaults = await get_plant_default(name)
    if defaults:
        w, f, t = defaults
    else:
        w, f, t = 7, 30, 365

    text = (
        f"🌱 {name}\n"
        f"💧 Полив через: {days_until(lw, w)} дней\n"
        f"🍀 Подкормка через: {days_until(lf, f)} дней\n"
        f"🪴 Пересадка через: {days_until(lt, t)} дней\n"
    )
    if notes:
        text += f"\nЗаметка: {notes}"

    await message.answer(text)


@router.message(Command("note"))
async def note(message: Message):
    args = message.get_arg().split(maxsplit=1)
    if len(args) < 2:
        return await message.answer("Использование: /note <растение> <текст>")
    name = args[0].lower()
    text = args[1]
    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Растение не найдено")

    await update_notes(message.from_user.id, name, text)
    await message.answer("Заметка сохранена")