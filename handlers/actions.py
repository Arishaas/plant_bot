from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from plant_states import AddPlant, DeletePlant
from database import add_user_plant, get_user_plants, delete_plant

router = Router()


async def start_action(message: Message, state: FSMContext, prompt_text: str, new_state):
    current_state = await state.get_state()
    if current_state:
        return await message.answer("⚠️ Сначала завершите текущую операцию!")
    await message.answer(prompt_text)
    await state.set_state(new_state)


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
    plants = await get_user_plants(message.from_user.id)
    plant_names = [p[0].lower() for p in plants]

    if name in plant_names:
        await state.update_data(duplicate_name=name)
        await state.set_state(AddPlant.waiting_for_duplicate_confirm)
        return await message.answer(
            f"⚠️ Растение «{name}» уже есть в списке.\n"
            "Добавить ещё одно с новым именем? (да/нет)"
        )

    await add_user_plant(message.from_user.id, name)
    await message.answer(f"➕🌺 Растение добавлено: {name}")
    await state.clear()


@router.message(AddPlant.waiting_for_duplicate_confirm)
async def add_duplicate_confirm(message: Message, state: FSMContext):
    answer = message.text.strip().lower()
    if answer not in {"да", "нет", "yes", "no"}:
        return await message.answer("Напишите «да» или «нет».")

    if answer in {"нет", "no"}:
        await message.answer("Ок, не добавляю.")
        await state.clear()
        return

    data = await state.get_data()
    base_name = data.get("duplicate_name", "").strip().lower()
    if not base_name:
        await message.answer("❌ Не удалось определить название. Попробуйте снова.")
        await state.clear()
        return

    plants = await get_user_plants(message.from_user.id)
    plant_names = {p[0].lower() for p in plants}

    idx = 2
    new_name = f"{base_name} {idx}"
    while new_name in plant_names:
        idx += 1
        new_name = f"{base_name} {idx}"

    await add_user_plant(message.from_user.id, new_name)
    await message.answer(f"➕🌺 Добавлено как: {new_name}")
    await state.clear()


@router.message(lambda m: m.text == "🌺 Мои растения")
async def show_plants(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        return await message.answer("⚠️ Сначала завершите текущую операцию!")

    plants = await get_user_plants(message.from_user.id)
    if not plants:
        return await message.answer("🌱 У вас пока нет растений")

    text = "🌺 Ваши растения:\n\n"
    for idx, plant in enumerate(plants, start=1):
        text += f"{idx}. {plant[0]}\n"

    await message.answer(text)


@router.message(lambda m: m.text == "❌🗑 Удаление растения")
async def delete_start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        return await message.answer("⚠️ Сначала завершите текущую операцию!")

    plants = await get_user_plants(message.from_user.id)
    if not plants:
        return await message.answer("🌱 У вас пока нет растений для удаления")

    plant_names = [p[0] for p in plants]
    text = "🗑 Выберите растение для удаления (введите точное название):\n"
    text += "\n".join(plant_names)
    await message.answer(text)
    await state.set_state(DeletePlant.waiting_for_name)


@router.message(DeletePlant.waiting_for_name)
async def delete_finish(message: Message, state: FSMContext):
    name = message.text.strip().lower()
    plants = await get_user_plants(message.from_user.id)
    plant_names = [p[0].lower() for p in plants]
    if name not in plant_names:
        return await message.answer("❌ Растение не найдено. Введите точное название")

    await delete_plant(message.from_user.id, name)
    await message.answer(f"🗑 Растение удалено: {name}")
    await state.clear()
