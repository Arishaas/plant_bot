from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from plant_states import TransplantPlant, WaterPlant, FeedPlant
from database import update_user_date, get_user_plant
from utils import pars_datetoken

router = Router()


@router.message(lambda m: m.text == "💧 Полив растения")
async def water_plant(message: Message, state: FSMContext):
    await message.answer("💧 Какое растения полили?")
    await state.set_state(WaterPlant.waiting_for_name)


@router.message(WaterPlant.waiting_for_name)
async def water_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()
    row = await get_user_plant(message.from_user.id, name)

    if not row:
        return await message.answer("❌ Растение не найдено")

    today = pars_datetoken("today")
    await update_user_date(message.from_user.id, name, "last_water", today)

    await message.answer(f"💧 Полив обновлен: {name}")
    await state.clear()


@router.message(lambda m: m == "🧪 Подкормка")
async def feed_plant(message: Message, state: FSMContext):
    await message.answer("🧪🌺 В какое растение добавлена подкормка?")
    await state.set_state(FeedPlant.warning_for_name)


@router.message(FeedPlant.warning_for_name)
async def feed_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("❌ Растение не найдено")

    today = pars_datetoken("today")
    await update_user_date(message.from_user.id, name, "last_feed", today)

    await message.answer(f"🧪  Подкормка обновлена: {name}")
    await state.clear()


@router.message(lambda m: m == "🔄🌱 Пересадка")
async def transplant_plant(message: Message, state: FSMContext):
    await message.answer("🔄🌱 Какое растение пересажено?")
    await state.set_state(TransplantPlant.waiting_for_name)


@router.message(TransplantPlant.waiting_for_name)
async def transplant_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()

    row = await get_user_plant(message.from_user.id, name)
    if not row:
        return await message.answer("❌ Растение не найдено")

    today = pars_datetoken("today")
    await update_user_date(message.from_user.id, name, "last_transplant", today)

    await message.answer(f"🔄🌱 Пересадка обновлена {name}")
    await state.clear()

