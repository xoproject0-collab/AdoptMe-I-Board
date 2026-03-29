from aiogram.types import CallbackQuery, Message
from keyboards.menus import trade_options_menu
from services.trade_service import calculate_value, trade_result

# Словарь текущих трейдов (user_id -> список питомцев)
user_trades = {}
all_trades = []

async def trade_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    if data == "create_trade":
        user_trades[user_id] = []
        await callback.message.answer("➕ Добавь питомцев в трейд! Используй /add_pet <имя> <value>")
        await callback.answer()
    elif data == "view_trades":
        if not all_trades:
            await callback.message.answer("📋 Нет опубликованных трейдов.")
        else:
            msg = "📋 Все трейды:\n\n"
            for t in all_trades:
                msg += f"Пользователь {t['user']}:\n"
                for p in t["pets"]:
                    msg += f"- {p['name']} ({p['value']})\n"
                msg += f"Value: {calculate_value(t['pets'])}\n\n"
            await callback.message.answer(msg)
        await callback.answer()
    elif data == "my_trades":
        user_trade = [t for t in all_trades if t["user"] == user_id]
        if not user_trade:
            await callback.message.answer("📦 У тебя нет трейдов.")
        else:
            msg = "👤 Мои трейды:\n\n"
            for t in user_trade:
                for p in t["pets"]:
                    msg += f"- {p['name']} ({p['value']})\n"
                msg += f"Value: {calculate_value(t['pets'])}\n\n"
            await callback.message.answer(msg)
        await callback.answer()
    elif data.startswith("option_"):
        await callback.message.answer(f"Выбрана опция: {data.split('_')[1].capitalize()}")
        await callback.answer()
