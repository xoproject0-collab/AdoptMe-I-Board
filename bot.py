# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, trade
from handlers import pets  # новый pets.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = "ВАШ_ТОКЕН_БОТА"

# --------------------------
# Инициализация бота
# --------------------------
bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# --------------------------
# Подключение роутеров
# --------------------------
dp.include_router(start.router)  # старый функционал /start
dp.include_router(trade.router)  # trade
dp.include_router(pets.router)   # pets.py

# --------------------------
# Настройка команд бота
# --------------------------
async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="trade", description="Начать трейд питомцев"),
        BotCommand(command="profit", description="Посчитать профит/лосс")
    ]
    await bot.set_my_commands(commands)

# --------------------------
# Планировщик для обновления питомцев каждые 10 минут
# --------------------------
scheduler = AsyncIOScheduler()

async def main():
    await set_commands()
    # --------------------------
    # Загружаем всех питомцев перед стартом
    # --------------------------
    try:
        await pets.load_all_pets()
        print("✅ Все питомцы загружены")
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")

    # Запускаем обновление каждые 10 минут
    scheduler.add_job(pets.load_all_pets, "interval", minutes=10, id="load_all_pets")
    scheduler.start()

    # --------------------------
    # Запуск polling
    # --------------------------
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
