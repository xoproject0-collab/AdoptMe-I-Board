# handlers/start.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="Список питомцев", callback_data="pets"),
        InlineKeyboardButton(text="Анализ трейдов", callback_data="trade")
    )
    await message.answer(
        "Привет! Я бот Adopt Me Board.\nВыбери действие ниже 👇",
        reply_markup=kb
    )
