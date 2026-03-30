from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот Adopt Me Board.\n"
        "Используй команды:\n"
        "/pets — список всех питомцев\n"
        "/trade — авто анализ трейдов"
    )
