from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Создать трейд", callback_data="create_trade")],
        [InlineKeyboardButton(text="📋 Смотреть трейды", callback_data="browse")]
    ])

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("🐾 Adopt Me Trade Bot V2 — с полным парсером питомцев", reply_markup=menu())
