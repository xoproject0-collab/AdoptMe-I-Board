import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, UPDATE_INTERVAL
from handlers import start, trade
from services.value_service import load_all_pets

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(trade.router)

    # Загружаем всех питомцев
    await load_all_pets()

    # Автообновление value каждые UPDATE_INTERVAL секунд
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", seconds=UPDATE_INTERVAL)
    scheduler.start()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
