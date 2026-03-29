from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать трейд", callback_data="create_trade")],
        [InlineKeyboardButton(text="Смотреть трейды", callback_data="view_trades")],
        [InlineKeyboardButton(text="Мои трейды", callback_data="my_trades")]
    ])
    return kb

def trade_options_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Fly ✨", callback_data="option_fly"),
         InlineKeyboardButton(text="Ride ⚡", callback_data="option_ride")],
        [InlineKeyboardButton(text="Neon 🌈", callback_data="option_neon"),
         InlineKeyboardButton(text="Mega 💥", callback_data="option_mega")]
    ])
    return kb
