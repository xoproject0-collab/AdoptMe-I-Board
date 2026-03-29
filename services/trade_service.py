# handlers/trade.py
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.menus import trade_quality_buttons
from services.value_service import get_value

# Словарь всех трейдов
all_trades = []  # { "user_id": 123, "pets": [...], "value": 50 }

class TradeFSM(StatesGroup):
    waiting_for_pet = State()
    waiting_for_quality = State()

async def create_trade_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TradeFSM.waiting_for_pet)
    await callback.message.answer(
        "Введите имя питомца для трейда:",
    )
    await callback.answer()

async def view_trades_handler(callback: CallbackQuery):
    if not all_trades:
        await callback.message.answer("📋 Пока нет трейдов")
    else:
        msg = "📋 Все трейды:\n"
        for t in all_trades:
            msg += f"{t['pets']} → Value: {t['value']}\n"
        await callback.message.answer(msg)
    await callback.answer()

async def my_trades_handler(callback: CallbackQuery):
    user_trades = [t for t in all_trades if t["user_id"] == callback.from_user.id]
    if not user_trades:
        await callback.message.answer("👤 У вас пока нет трейдов")
    else:
        msg = "👤 Ваши трейды:\n"
        for t in user_trades:
            msg += f"{t['pets']} → Value: {t['value']}\n"
        await callback.message.answer(msg)
    await callback.answer()
