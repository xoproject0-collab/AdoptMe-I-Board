from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(commands=["start"])
async def start_handler(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Создать трейд"))
    kb.add(KeyboardButton("Смотреть трейды"))
    await message.answer("Привет! Что делаем?", reply_markup=kb)
