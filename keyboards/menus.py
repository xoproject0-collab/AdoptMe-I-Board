# keyboards/menus.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Создать трейд", callback_data="create_trade")],
            [InlineKeyboardButton("Смотреть трейды", callback_data="view_trades")],
            [InlineKeyboardButton("Мои трейды", callback_data="my_trades")],
        ],
        row_width=1
    )
    return kb

def trade_quality_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Fly", callback_data="quality_fly"),
                InlineKeyboardButton("Ride", callback_data="quality_ride"),
            ],
            [
                InlineKeyboardButton("Neon", callback_data="quality_neon"),
                InlineKeyboardButton("Mega", callback_data="quality_mega"),
            ],
            [InlineKeyboardButton("Готово", callback_data="trade_done")]
        ]
    )
