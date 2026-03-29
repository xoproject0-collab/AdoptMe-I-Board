from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    # Зеленая кнопка "Создать трейд"
    kb.add(
        InlineKeyboardButton(
            text="Создать трейд", 
            callback_data="create_trade"
        )
    )
    # Синяя кнопка "Смотреть трейды"
    kb.add(
        InlineKeyboardButton(
            text="Смотреть трейды", 
            callback_data="view_trades"
        )
    )
    # Обычная кнопка "Мои трейды"
    kb.add(
        InlineKeyboardButton(
            text="Мои трейды", 
            callback_data="my_trades"
        )
    )
    return kb
