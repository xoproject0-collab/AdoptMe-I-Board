from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Создать трейд"))
    kb.add(KeyboardButton("Смотреть трейды"))

    await message.answer("Привет! Выбери действие:", reply_markup=kb)
