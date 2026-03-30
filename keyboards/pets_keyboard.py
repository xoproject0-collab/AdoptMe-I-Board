from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def pets_page(pets, page=0, per_page=10):
    kb = InlineKeyboardMarkup(row_width=2)
    start = page * per_page
    end = start + per_page
    for pet in pets[start:end]:
        kb.add(InlineKeyboardButton(pet["name"], callback_data=f"pet_{pet['id']}"))
    # Кнопки листания
    if page > 0:
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page-1}"))
    if end < len(pets):
        kb.add(InlineKeyboardButton("➡️ Вперёд", callback_data=f"page_{page+1}"))
    return kb

def modifiers_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Fly", callback_data="mod_Fly"),
        InlineKeyboardButton("Ride", callback_data="mod_Ride"),
    )
    kb.add(
        InlineKeyboardButton("Neon", callback_data="mod_Neon"),
        InlineKeyboardButton("Mega Neon", callback_data="mod_MegaNeon"),
    )
    kb.add(InlineKeyboardButton("✅ Готово", callback_data="mod_done"))
    return kb
