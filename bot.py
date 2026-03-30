import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import start, pets, trade

API_TOKEN = "8585113754:AAEuFxy-rHCCAvvxOdLcCtKej5g82MvLU1E"

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(pets.router)
    dp.include_router(trade.router)

    # Настройка команд
    await bot.set_my_commands([
        BotCommand(command="start", description="Приветствие и помощь"),
        BotCommand(command="pets", description="Список всех питомцев"),
        BotCommand(command="trade", description="Анализ трейдов")
    ])

    # Загружаем питомцев
    await pets.load_all_pets()

    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
