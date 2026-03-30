import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from handlers import start, trade, pets

TOKEN = "8585113754:AAEuFxy-rHCCAvvxOdLcCtKej5g82MvLU1E"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем все роутеры (handlers)
    dp.include_router(start.router)
    dp.include_router(trade.router)
    dp.include_router(pets.router)

    # Загружаем питомцев
    await pets.load_all_pets()

    # Настраиваем команды для бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="pets", description="Список всех питомцев"),
        BotCommand(command="trade", description="Анализ трейдов")
    ])

    print("🚀 Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
