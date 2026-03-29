from aiogram.types import Message

async def create_trade(message: Message):
    await message.answer("📝 Давай создадим трейд! (тут будет логика создания трейда)")

async def show_trades(message: Message):
    await message.answer("📋 Список всех трейдов (тут будет логика показа трейдов)")

async def my_trades(message: Message):
    await message.answer("📦 Твои трейды (тут будет логика твоих трейдов)")
