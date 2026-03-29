import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.text import Text  # <- правильный импорт для фильтра текста
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, VALUE_UPDATE_INTERVAL
from services.value_service import load_all_pets
from handlers.start import start
from handlers.trade import create_trade, my_trades, show_trades

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    print("[INFO] Бот запускается...")

    # Планировщик для обновления value
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", minutes=VALUE_UPDATE_INTERVAL)
    scheduler.start()

    # Подгружаем value питомцев сразу
    await load_all_pets()
    print("[INFO] Value питомцев загружено.")

    # Регистрация хэндлеров
    dp.message.register(start, Command(commands=["start"]))
    dp.message.register(create_trade, Text(text="➕ Создать трейд"))
    dp.message.register(show_trades, Text(text="📋 Смотреть трейды"))
    dp.message.register(my_trades, Text(text="📦 Мои трейды"))

    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
