from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Кнопка "Создать трейд"
@router.message(Text("Создать трейд"))
async def create_trade(message: Message):
    # Пример категорий питомцев
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Легендарные"))
    kb.add(KeyboardButton("Редкие"))
    kb.add(KeyboardButton("Обычные"))
    kb.add(KeyboardButton("Перейти к выбору что хочу получить"))

    await message.answer("Выбери категорию питомцев для трейда:", reply_markup=kb)

# Кнопка "Смотреть трейды"
@router.message(Text("Смотреть трейды"))
async def view_trades(message: Message):
    # Пока простой пример, потом подключим базу
    await message.answer("Здесь будет лента трейдов в формате: Что даёшь → Что хочешь")
