from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать", callback_data="create_trade")],
        [InlineKeyboardButton(text="📊 Смотреть трейды", callback_data="watch_trades")]
    ])

    await message.answer(
        "🔥 Adopt Me Trade Bot\n\nВыбирай действие:",
        reply_markup=kb
    )
