import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, VALUE_UPDATE_INTERVAL
from services.value_service import load_all_pets
from handlers.start import start
from keyboards.menus import main_menu

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрируем команду /start
dp.message.register(start, commands=["start"])

async def main():
    print("[INFO] Бот запускается...")

    # Планировщик для обновления value — запускаем внутри event loop
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", minutes=VALUE_UPDATE_INTERVAL)
    scheduler.start()

    # Сразу подгружаем value питомцев
    await load_all_pets()
    print("[INFO] Value питомцев загружено.")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
