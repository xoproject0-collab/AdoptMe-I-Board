# pets.py
import aiohttp
import asyncio
from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

API_URL = "https://adoptmevalues.gg/api/v1/values"
PAGE_LIMIT = 20  # столько питомцев на странице
MODIFIERS = ["Fly", "Ride", "Neon", "Mega Neon"]

# Хранение временного выбора питомцев по пользователям
user_selection = {}

# -------------------- Получение всех питомцев --------------------
async def fetch_all_pets():
    all_pets = []
    page = 1
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}?sortBy=position&limit={PAGE_LIMIT}&page={page}") as resp:
                data = await resp.json()
                pets = data.get("data", [])
                if not pets:
                    break
                all_pets.extend(pets)
                page += 1
    return all_pets

# -------------------- Клавиатура с питомцами --------------------
def make_pet_keyboard(pets, user_id):
    kb = InlineKeyboardMarkup(row_width=2)
    for pet in pets:
        kb.insert(
            InlineKeyboardButton(
                f"{pet['name']} ({pet['rarity']})",
                callback_data=f"select_{user_id}_{pet['id']}"
            )
        )
    # Кнопки модификаторов
    mod_buttons = [InlineKeyboardButton(m, callback_data=f"mod_{user_id}_{m}") for m in MODIFIERS]
    kb.add(*mod_buttons)
    kb.add(InlineKeyboardButton("▶ Перейти к выбору что хочу получить", callback_data=f"next_{user_id}"))
    return kb

# -------------------- Начало выбора питомцев --------------------
@router.callback_query(F.data.startswith("choose_pets"))
async def choose_pets(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_selection[user_id] = {"give": [], "want": [], "current_mods": []}
    pets = await fetch_all_pets()
    user_selection[user_id]["all_pets"] = pets
    kb = make_pet_keyboard(pets[:PAGE_LIMIT], user_id)
    await callback.message.edit_text("Выберите питомцев, которых отдаёте:", reply_markup=kb)

# -------------------- Выбор питомца --------------------
@router.callback_query(F.data.startswith("select_"))
async def select_pet(callback: CallbackQuery):
    _, user_id_str, pet_id = callback.data.split("_")
    user_id = int(user_id_str)
    pets = user_selection[user_id]["all_pets"]
    pet = next((p for p in pets if str(p["id"]) == pet_id), None)
    if pet:
        mods = user_selection[user_id]["current_mods"]
        user_selection[user_id]["give"].append({"id": pet["name"], "mods": mods.copy()})
        user_selection[user_id]["current_mods"].clear()
        await callback.answer(f"Вы выбрали {pet['name']} с модификаторами: {', '.join(mods) if mods else 'нет'}")

# -------------------- Выбор модификатора --------------------
@router.callback_query(F.data.startswith("mod_"))
async def select_modifier(callback: CallbackQuery):
    _, user_id_str, mod = callback.data.split("_")
    user_id = int(user_id_str)
    if mod not in user_selection[user_id]["current_mods"]:
        user_selection[user_id]["current_mods"].append(mod)
    await callback.answer(f"Модификатор {mod} добавлен")

# -------------------- Переход к выбору что получаем --------------------
@router.callback_query(F.data.startswith("next_"))
async def next_step(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await callback.message.edit_text(
        "Теперь выберите питомцев, которых хотите получить (работает так же, как отдаёте).",
        reply_markup=make_pet_keyboard(user_selection[user_id]["all_pets"][:PAGE_LIMIT], user_id)
    )
    # Следующие клики будут добавлять в user_selection[user_id]["want"]

# -------------------- Публикация трейда --------------------
@router.callback_query(F.data.startswith("publish_"))
async def publish_trade_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    give = user_selection[user_id]["give"]
    want = user_selection[user_id]["want"]
    if not give or not want:
        await callback.answer("Вы должны выбрать хотя бы одного питомца для отдачи и получения!")
        return
    from handlers import trade
    trade_id = trade.publish_trade(user_id, give, want)
    await callback.message.edit_text(f"Трейд опубликован! ID: {trade_id}")
    # очищаем временный выбор
    user_selection[user_id] = {"give": [], "want": [], "current_mods": []}
