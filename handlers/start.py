from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🔥 AdoptMe BOT\n\n"
        "📦 /pets — список питомцев\n"
        "📊 /trade — анализ трейда\n"
    )
