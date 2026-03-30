import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, trade, pets

BOT_TOKEN = "8585113754:AAEuFxy-rHCCAvvxOdLcCtKej5g82MvLU1E"

# УБИВАЕТ старые подключения
await bot.delete_webhook(drop_pending_updates=True)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(trade.router)
    dp.include_router(pets.router)

    # загрузка питомцев при старте
    await pets.load_all_pets()

    print("🚀 Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
