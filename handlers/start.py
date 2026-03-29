from aiogram import types
from keyboards.menus import main_menu

async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "С помощью этого бота ты можешь создавать трейды Adopt Me.\n"
        "Выбирай питомцев, их качества (Fly, Ride, Neon, Mega) и публикуй трейды!",
        reply_markup=main_menu()
    )
