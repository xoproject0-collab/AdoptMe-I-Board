import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, UPDATE_INTERVAL
from handlers import start, pets
from services.value_service import load_all_pets
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(pets.router)

    # Загружаем всех питомцев сразу
    await load_all_pets()

    # Автообновление value каждые 10 минут
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", seconds=UPDATE_INTERVAL)
    scheduler.start()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
