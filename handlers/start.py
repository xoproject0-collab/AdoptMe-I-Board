from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привет! Я бот Adopt Me Board.\n"
        "Используй команды:\n"
        "/pets — список всех питомцев\n"
        "/trade — авто анализ трейдов"
    )
    await message.answer(text)
