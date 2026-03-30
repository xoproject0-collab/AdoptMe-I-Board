from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(commands=["trade"])
async def trade_command(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Анализ всех трейдов", callback_data="analyze_all"),
        InlineKeyboardButton(text="Добавить новый трейд", callback_data="add_trade"),
    )
    await message.answer("Выберите действие для трейдов:", reply_markup=keyboard)
