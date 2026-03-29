import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, VALUE_UPDATE_INTERVAL
from services.value_service import load_all_pets
from handlers.start import start
from keyboards.menus import main_menu
from handlers.trade import create_trade, show_trades, my_trades

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

    # Регистрируем команды
    dp.message.register(start, Command(commands=["start"]))

    # Регистрируем кнопки
    dp.message.register(create_trade, lambda msg: msg.text == "🟩 Создать трейд")
    dp.message.register(show_trades, lambda msg: msg.text == "🟦 Смотреть трейды")
    dp.message.register(my_trades, lambda msg: msg.text == "🟧 Мои трейды")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
