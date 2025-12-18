from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.command import CommandObject  # ← обязательно импортируем
from utils import pars_datetoken, days_until
from database import (
    get_user_plant, update_user_date, update_notes, get_plant_default
)

router = Router()


@router.message(Command("water"))
async def water(message: Message, command: CommandObject):
    name = (command.args or "").strip().lower()
    if not name:
        return await message.answer("Использование: /water <название>")
    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")
    today = pars_datetoken("today")
    await update_user_date(message.from_user.id, name, "last_water", today)
    await message.answer(f"✅ Полив обновлён для: {name} — {today}")


@router.message(Command("feed"))
async def feed(message: Message, command: CommandObject):
    args = (command.args or "").split()
    if not args:
        return await message.answer("Использование: /feed <название> [дата]")

    name = args[0].lower()
    date_token = args[1] if len(args) > 1 else "today"
    date_iso = pars_datetoken(date_token)
    if not date_iso:
        return await message.answer("Неверная дата. Используйте YYYY-MM-DD или 'today'")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    await update_user_date(message.from_user.id, name, "last_feed", date_iso)
    await message.answer(f"✅ Подкормка обновлена для: {name} — {date_iso}")


@router.message(Command("transplant"))
async def transplant(message: Message, command: CommandObject):
    args = (command.args or "").split()
    if not args:
        return await message.answer("Использование: /transplant <название> [дата]")

    name = args[0].lower()
    date_token = args[1] if len(args) > 1 else "today"
    date_iso = pars_datetoken(date_token)
    if not date_iso:
        return await message.answer("Неверная дата. Используйте YYYY-MM-DD или 'today'")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    await update_user_date(message.from_user.id, name, "last_trans", date_iso)
    await message.answer(f"✅ Пересадка обновлена для: {name} — {date_iso}")


@router.message(Command("status"))
async def status(message: Message, command: CommandObject):
    name = (command.args or "").strip().lower()
    if not name:
        return await message.answer("Использование: /status <название>")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Нет такого растения")

    _, lw, lf, lt, notes = row
    defaults = await get_plant_default(name)
    w, f, t = defaults if defaults else (7, 30, 365)

    text = (
        f"🌱 {name}\n"
        f"💧 Полив через: {max(0, days_until(lw, w))} дн.\n"
        f"🍀 Подкормка через: {max(0, days_until(lf, f))} дн.\n"
        f"🪴 Пересадка через: {max(0, days_until(lt, t))} дн."
    )
    if notes:
        text += f"\n📝 Заметка: {notes}"

    await message.answer(text)


@router.message(Command("note"))
async def note(message: Message, command: CommandObject):
    if not command.args or len(command.args.split()) < 2:
        return await message.answer("Использование: /note <растение> <текст>")

    name, text = command.args.split(maxsplit=1)
    name = name.lower()

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("Растение не найдено")

    await update_notes(message.from_user.id, name, text)
    await message.answer("✅ Заметка сохранена")