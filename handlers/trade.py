from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.value_service import ALL_PETS

router = Router()

user_trade = {}

# === МЕНЮ ===
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Создать трейд", callback_data="create_trade")],
        [InlineKeyboardButton(text="📊 Смотреть трейды", callback_data="watch_trades")],
    ])


# === СОЗДАНИЕ ===
@router.callback_query(F.data == "create_trade")
async def create_trade(call: CallbackQuery):
    user_trade[call.from_user.id] = {
        "offer": [],
        "want": []
    }

    await call.message.edit_text(
        "📦 Выбери питомца (что ТЫ даёшь):",
        reply_markup=pets_keyboard(0)
    )


# === КНОПКИ ПИТОМЦЕВ ===
def pets_keyboard(page):
    per_page = 6
    start = page * per_page
    end = start + per_page

    buttons = []

    for pet in ALL_PETS[start:end]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{pet['name']} ({pet['value']})",
                callback_data=f"pet_{pet['name']}"
            )
        ])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page+1}"))

    buttons.append(nav)

    buttons.append([
        InlineKeyboardButton(text="➡️ К выбору WANT", callback_data="to_want")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === ВЫБОР ПИТОМЦА ===
@router.callback_query(F.data.startswith("pet_"))
async def add_pet(call: CallbackQuery):
    pet_name = call.data.split("_")[1]

    user_trade[call.from_user.id]["offer"].append(pet_name)

    await call.answer(f"Добавлен {pet_name}")


# === СТРАНИЦЫ ===
@router.callback_query(F.data.startswith("page_"))
async def change_page(call: CallbackQuery):
    page = int(call.data.split("_")[1])

    await call.message.edit_reply_markup(
        reply_markup=pets_keyboard(page)
    )


# === WANT ===
@router.callback_query(F.data == "to_want")
async def to_want(call: CallbackQuery):
    await call.message.edit_text(
        "🎯 Теперь выбери что ХОЧЕШЬ:",
        reply_markup=pets_keyboard(0)
    )


# === ПРОСМОТР ===
@router.callback_query(F.data == "watch_trades")
async def watch_trades(call: CallbackQuery):
    data = user_trade.get(call.from_user.id)

    if not data:
        await call.message.answer("Нет трейдов")
        return

    await call.message.answer(
        f"📦 Ты даёшь: {', '.join(data['offer'])}\n"
        f"🎯 Хочешь: {', '.join(data['want'])}"
    )
