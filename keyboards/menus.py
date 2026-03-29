from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🟩 Создать трейд")],
            [KeyboardButton(text="🟦 Смотреть трейды")],
            [KeyboardButton(text="🟧 Мои трейды")]
        ],
        resize_keyboard=True
    )
    return kb
