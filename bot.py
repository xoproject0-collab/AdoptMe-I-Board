# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp

from config import TOKEN, VALUE_UPDATE_INTERVAL
from services.value_service import load_all_pets
from handlers.start import start
from handlers.trade import create_trade_handler, view_trades_handler, my_trades_handler

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def clear_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            data = await resp.json()
            if data.get("ok"):
                print("[INFO] Старый webhook успешно удалён")
            else:
                print(f"[WARNING] Не удалось удалить webhook: {data}")

async def main():
    await clear_webhook()

    # Планировщик value
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", minutes=VALUE_UPDATE_INTERVAL)
    scheduler.start()

    await load_all_pets()
    print("[INFO] Value питомцев загружено.")

    # Регистрируем команду /start
    dp.message.register(start, Command(commands=["start"]))

    # Callback кнопки трейда
    dp.callback_query.register(create_trade_handler, lambda c: c.data == "create_trade")
    dp.callback_query.register(view_trades_handler, lambda c: c.data == "view_trades")
    dp.callback_query.register(my_trades_handler, lambda c: c.data == "my_trades")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
