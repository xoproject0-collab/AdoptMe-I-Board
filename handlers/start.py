from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я бот Adopt Me Board.\n"
        "Используй команды:\n"
        "/pets — список всех питомцев\n"
        "/trade — авто анализ трейдов"
    )
    await message.answer(text)
