from aiogram.types import Message
from services.value_service import get_value
from services.trade_service import calculate_value, trade_result

# Списки трейдов
trades = []  # все трейды
my_trades_dict = {}  # трейды по пользователю

async def create_trade(message: Message):
    # Простейший пример создания трейда
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Для простоты: берём фиктивного питомца
    pets = [{"name": "Dog", "value": get_value("dog")}]

    trade = {"user": user_name, "pets": pets}
    trades.append(trade)
    my_trades_dict.setdefault(user_id, []).append(trade)

    total_value = calculate_value(pets)
    await message.answer(
        f"✅ Трейд создан!\nПитомцы: {[p['name'] for p in pets]}\n"
        f"Суммарная value: {total_value}"
    )

async def show_trades(message: Message):
    if not trades:
        await message.answer("📋 Пока нет опубликованных трейдов.")
        return
    text = "📋 Список всех трейдов:\n\n"
    for i, t in enumerate(trades, 1):
        pet_names = [p['name'] for p in t['pets']]
        value = calculate_value(t['pets'])
        text += f"{i}. {t['user']} предлагает {pet_names} (Value: {value})\n"
    await message.answer(text)

async def my_trades(message: Message):
    user_id = message.from_user.id
    user_trades = my_trades_dict.get(user_id, [])
    if not user_trades:
        await message.answer("📦 У тебя пока нет трейдов.")
        return
    text = "📦 Твои трейды:\n\n"
    for i, t in enumerate(user_trades, 1):
        pet_names = [p['name'] for p in t['pets']]
        value = calculate_value(t['pets'])
        text += f"{i}. {pet_names} (Value: {value})\n"
    await message.answer(text)
