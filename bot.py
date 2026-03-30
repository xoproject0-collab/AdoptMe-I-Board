import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, trade
from services.value_service import load_all_pets
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- Настройки ---
logging.basicConfig(level=logging.INFO)
UPDATE_INTERVAL = 600  # если у тебя это в config, можно импортировать

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")  # <-- убедись, что имя переменной совпадает с Railway

if not TOKEN:
    raise ValueError("⚠️ Переменная окружения TOKEN не установлена! Добавьте её в Railway Variables.")

# --- Главная функция ---
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(trade.router)

    # Загружаем всех питомцев сразу
    await load_all_pets()

    # Автообновление value каждые UPDATE_INTERVAL секунд
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", seconds=UPDATE_INTERVAL)
    scheduler.start()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
