from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔘 Создать трейд", callback_data="create_trade"),
        InlineKeyboardButton("📄 Мои трейды", callback_data="my_trades"),
    )
    kb.add(
        InlineKeyboardButton("❤️ Избранное", callback_data="favorites"),
        InlineKeyboardButton("🔍 Поиск питомца", callback_data="search_pet"),
    )
    return kb
