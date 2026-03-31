from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌺 Мои растения")],
        [KeyboardButton(text="➕ Добавить растение")],
        [KeyboardButton(text="💧Полив растения"), KeyboardButton(text="🧪 Подкормка растения")],
        [KeyboardButton(text="🔄 Пересадка растения")],
        [KeyboardButton(text="❌🗑 Удаление растения")]
    ],
    resize_keyboard=True
)
