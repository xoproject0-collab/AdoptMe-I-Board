import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, trade, pets  # pets добавлен

API_TOKEN = "8585113754:AAEuFxy-rHCCAvvxOdLcCtKej5g82MvLU1E"

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Подключаем старые роутеры
    dp.include_router(start.router)
    dp.include_router(trade.router)

    # Подключаем новый pets роутер
    dp.include_router(pets.router)

    # Загружаем всех питомцев перед стартом
    await pets.load_all_pets()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
