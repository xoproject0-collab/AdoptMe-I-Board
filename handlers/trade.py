from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("trade"))
async def cmd_trade(message: Message):
    # Пример анализа трейдов
    await message.answer("Анализ трейдов выполнен ✅")
