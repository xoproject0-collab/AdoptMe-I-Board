from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать трейд", callback_data="create_trade")],
            [InlineKeyboardButton(text="Смотреть трейды", callback_data="view_trades")],
            [InlineKeyboardButton(text="Мои трейды", callback_data="my_trades")],
        ]
    )
    return kb
