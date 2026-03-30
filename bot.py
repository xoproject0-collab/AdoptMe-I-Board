import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, pets, trade

BOT_TOKEN = "8585113754:AAEuFxy-rHCCAvvxOdLcCtKej5g82MvLU1E"

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем routers
    dp.include_router(start.router)
    dp.include_router(pets.router)
    dp.include_router(trade.router)

    # Загружаем питомцев перед стартом
    await pets.load_all_pets()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
