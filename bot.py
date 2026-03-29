import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import Command
from handlers.start import start
from handlers.trade import trade_handler
from services.value_service import load_all_pets, VALUE_UPDATE_INTERVAL

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("[INFO] Бот запускается...")

    # Планировщик для обновления value
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", minutes=VALUE_UPDATE_INTERVAL)
    scheduler.start()

    # Загружаем value питомцев сразу
    await load_all_pets()
    print("[INFO] Value питомцев загружено.")

    # Регистрируем обработчики
    dp.message.register(start, Command("start"))
    dp.callback_query.register(trade_handler)  # все кнопки трейда

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
