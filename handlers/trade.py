from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.value_service import ALL_PETS

router = Router()

USER_TRADES = {}  # {user_id: {"give": [], "want": []}}

# Шаг 1: выбрать отдаваемых питомцев
@router.message(F.text == "Создать трейд")
async def trade_start(message: Message):
    USER_TRADES[message.from_user.id] = {"give": [], "want": []}
    await show_categories(message, "give")

async def show_categories(event, step):
    kb = InlineKeyboardMarkup()
    for category in ALL_PETS.keys():
        kb.add(InlineKeyboardButton(category.capitalize(), callback_data=f"{step}_cat_{category}"))
    await event.answer("Выбери категорию питомцев:", reply_markup=kb)

# Шаг 2: выбрать питомцев в категории
@router.callback_query()
async def category_selected(query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data  # например: give_cat_legendary
    step, _, category = data.split("_", 2)

    kb = InlineKeyboardMarkup()
    for pet in ALL_PETS[category]:
        kb.add(InlineKeyboardButton(pet["name"], callback_data=f"{step}_pet_{pet['name']}"))
    kb.add(InlineKeyboardButton("Готово / Дальше", callback_data=f"{step}_done"))
    await query.message.edit_text(f"Категория: {category}", reply_markup=kb)

# Шаг 3: выбрать питомцев
@router.callback_query()
async def pet_selected(query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    if "_done" in data:
        step = data.split("_")[0]
        if step == "give":
            await show_categories(query, "want")  # перейти к желаемым
        else:
            await publish_trade(query)
        return

    step, _, pet_name = data.split("_", 2)
    USER_TRADES[user_id][step].append(pet_name)
    await query.answer(f"{pet_name} добавлен(а)")

async def publish_trade(query: CallbackQuery):
    user_id = query.from_user.id
    trade = USER_TRADES[user_id]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Мои трейды", callback_data="my_trades")],
        [InlineKeyboardButton("Удалить трейд", callback_data=f"delete_{user_id}")]
    ])

    text = f"Отдаю: {', '.join(trade['give'])}\nХочу: {', '.join(trade['want'])}"
    await query.message.edit_text(text, reply_markup=kb)
