from aiogram.types import Message
from services.value_service import get_value
from services.trade_service import calculate_value, trade_result

# Простейший пример структуры
trades = []  # список всех трейдов
my_trades_dict = {}  # трейды по пользователю


async def create_trade(message: Message):
    await message.answer(
        "🛠 Здесь логика создания трейда.\n"
        "Например: пользователь выбирает питомцев и их качества, и трейд сохраняется."
    )


async def show_trades(message: Message):
    if not trades:
        await message.answer("📋 Пока нет опубликованных трейдов.")
        return
    text = "📋 Список всех трейдов:\n\n"
    for i, t in enumerate(trades, 1):
        text += f"{i}. {t['user']} предлагает {len(t['pets'])} питомцев\n"
    await message.answer(text)


async def my_trades(message: Message):
    user_id = message.from_user.id
    user_trades = my_trades_dict.get(user_id, [])
    if not user_trades:
        await message.answer("📦 У тебя пока нет трейдов.")
        return
    text = "📦 Твои трейды:\n\n"
    for i, t in enumerate(user_trades, 1):
        text += f"{i}. {len(t['pets'])} питомцев\n"
    await message.answer(text)
