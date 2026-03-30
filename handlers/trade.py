# trade.py
from aiogram import Router, types
from handlers import pets

router = Router()

@router.message(commands=["trade"])
async def cmd_trade(message: types.Message):
    await message.answer("Выберите питомцев для трейда (пока пример):")
    kb = pets.build_pets_keyboard(page=0)
    await message.answer("Список питомцев:", reply_markup=kb)

@router.message(commands=["profit"])
async def cmd_profit(message: types.Message):
    await message.answer("Расчёт профита / лосса ещё не реализован")
