from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from plant_states import WaterPlant, FeedPlant, TransplantPlant, AddPlant
from database import get_user_plant, update_user_date, add_user_plant
from utils import pars_datetoken

router = Router()


async def start_action(message: Message, state: FSMContext, prompt_text: str, new_state):
    await state.clear()
    await message.answer(prompt_text)
    await state.set_state(new_state)


async def update_plant_action(message: Message, state: FSMContext, field: str, success_text: str):
    parts = message.text.strip().split()
    if not parts:
        return await message.answer("❌ Введите название растения")

    if len(parts) > 1:
        parsed_date = pars_datetoken(parts[-1])
        if parsed_date:
            name = " ".join(parts[:-1]).lower()
            date_iso = parsed_date
        else:
            # Если дата не указана, считаем весь текст названием и ставим сегодняшнюю дату.
            name = " ".join(parts).lower()
            date_iso = pars_datetoken("today")
    else:
        name = parts[0].lower()
        date_iso = pars_datetoken("today")

    if not date_iso:
        return await message.answer("❌ Неверная дата. Пример: 'today' или 'YYYY-MM-DD'")

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("❌ Растение не найдено")

    await update_user_date(message.from_user.id, name, field, date_iso)
    await message.answer(f"{success_text}\n🌿 {name}\n📅 {date_iso}")
    await state.clear()


@router.message(lambda m: m.text == "💧Полив растения")
async def water_plant(message: Message, state: FSMContext):
    await start_action(
        message,
        state,
        "💧 Введите название растения для полива (можно добавить дату через пробел, например: Ромашка today)",
        WaterPlant.waiting_for_name
    )


@router.message(WaterPlant.waiting_for_name)
async def water_finish(message: Message, state: FSMContext):
    await update_plant_action(message, state, "last_water", "💧 Готово! Полив отмечен.")


@router.message(lambda m: m.text == "🧪 Подкормка растения")
async def feed_plant(message: Message, state: FSMContext):
    await start_action(
        message,
        state,
        "🧪 Введите название растения для подкормки (можно добавить дату через пробел, например: Ромашка today)",
        FeedPlant.waiting_for_name
    )


@router.message(FeedPlant.waiting_for_name)
async def feed_finish(message: Message, state: FSMContext):
    await update_plant_action(message, state, "last_feed", "🧪 Готово! Подкормка отмечена.")


@router.message(lambda m: m.text == "🔄 Пересадка растения")
async def transplant_plant(message: Message, state: FSMContext):
    await start_action(
        message,
        state,
        "🔄 Введите название растения для пересадки (можно добавить дату через пробел, например: Ромашка today)",
        TransplantPlant.waiting_for_name
    )


@router.message(TransplantPlant.waiting_for_name)
async def transplant_finish(message: Message, state: FSMContext):
    await update_plant_action(message, state, "last_trans", "🔄 Готово! Пересадка отмечена.")


@router.message(lambda m: m.text == "➕ Добавить растение")
async def add_plant_start(message: Message, state: FSMContext):
    await start_action(
        message,
        state,
        "🌱 Введите название нового растения",
        AddPlant.waiting_for_name
    )


@router.message(AddPlant.waiting_for_name)
async def add_plant_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()
    await add_user_plant(message.from_user.id, name)
    await message.answer(f"➕ Отлично, растение добавлено: {name}")
    await state.clear()
