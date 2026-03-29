import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, VALUE_UPDATE_INTERVAL
from services.value_service import load_all_pets, get_value, pets
from handlers.start import start
from keyboards.menus import main_menu

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Планировщик для обновления value
scheduler = AsyncIOScheduler()
scheduler.add_job(load_all_pets, "interval", minutes=VALUE_UPDATE_INTERVAL)
scheduler.start()

# Регистрируем команду /start
dp.register_message_handler(start, commands=["start"])

async def on_startup(dp):
    print("[INFO] Бот запускается...")
    await load_all_pets()
    print("[INFO] Value питомцев загружено.")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)