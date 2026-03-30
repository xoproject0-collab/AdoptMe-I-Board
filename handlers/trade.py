from aiogram import Router, types
from handlers import pets  # правильно импортируем ALL_PETS
# from handlers.pets import ALL_PETS  # теперь можно через pets.ALL_PETS

router = Router()

@router.message()
async def trade_example(message: types.Message):
    await message.answer(f"Всего питомцев в системе: {len(pets.ALL_PETS)}")
