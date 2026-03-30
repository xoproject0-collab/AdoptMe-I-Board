from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Смотреть трейды")],
            [KeyboardButton(text="➕ Создать трейд")],
            [KeyboardButton(text="📂 Мои трейды")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🚀 Добро пожаловать в Adopt Me Trade Bot!\n\n"
        "Выбирай действие:",
        reply_markup=kb
    )
    
