from aiogram import Router, types
from aiogram.filters import Command
from handlers.pets import ALL_PETS

router = Router()

@router.message(Command("trade"))
async def cmd_trade(message: types.Message):
    if not ALL_PETS:
        await message.answer("Питомцы ещё не загружены, попробуйте чуть позже.")
        return
    # пример авто анализа: просто выводим питомков с NR или Ride
    profit_pets = [p for p in ALL_PETS if p.get("fly") or p.get("ride")]
    if not profit_pets:
        await message.answer("Не найдено подходящих питомцев для трейда.")
        return
    text = "Потенциальные трейд питомцы:\n" + "\n".join([p["name"] for p in profit_pets])
    await message.answer(text)
