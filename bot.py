import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, trade
import handlers.pets as pets  # сервис для питомцев

BOT_TOKEN = "YOUR_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start.router)
dp.include_router(trade.router)

async def main():
    # Загружаем питомцев
    await pets.load_all_pets()  # исправлен отступ и вызов

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
