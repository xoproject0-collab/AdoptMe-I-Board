from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Создать трейд", callback_data="create_trade")],
        [InlineKeyboardButton("Смотреть трейды", callback_data="view_trades")],
        [InlineKeyboardButton("Мои трейды", callback_data="my_trades")]
    ])
    return kb

def trade_options_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Fly ✨", callback_data="option_fly"),
         InlineKeyboardButton("Ride ⚡", callback_data="option_ride")],
        [InlineKeyboardButton("Neon 🌈", callback_data="option_neon"),
         InlineKeyboardButton("Mega 💥", callback_data="option_mega")]
    ])
    return kb
