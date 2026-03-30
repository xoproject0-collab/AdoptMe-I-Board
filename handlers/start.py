from aiogram import Router
from aiogram.types import Message
from keyboards.main_keyboard import main_menu

router = Router()

@router.message()
async def cmd_start(message: Message):
    await message.answer("Привет! Добро пожаловать в Adopt Me трейдер бот 🚀", reply_markup=main_menu())
