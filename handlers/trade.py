# trade.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from handlers.pets import ALL_PETS  # новый pets.py

router = Router()  # 🔹 создаём router для trade

# ----------------------
# Inline кнопки для трейда
# ----------------------

@router.message(F.text == "/trade")
async def start_trade(message: Message):
    if not ALL_PETS:
        await message.answer("Питомцы ещё загружаются, подождите...")
        return
    kb = InlineKeyboardMarkup(row_width=2)
    for pet in list(ALL_PETS.values())[:10]:
        kb.add(InlineKeyboardButton(pet["name"], callback_data=f"trade_pet_{pet['id']}"))
    await message.answer("Выберите питомца для трейда:", reply_markup=kb)


@router.callback_query(F.data.startswith("trade_pet_"))
async def select_trade_pet(call: CallbackQuery):
    pet_id = call.data.split("_")[2]
    pet = ALL_PETS.get(pet_id)
    if not pet:
        await call.answer("Питомец не найден 😢")
        return
    # Кнопки для модификаторов
    kb = InlineKeyboardMarkup(row_width=2)
    for mod in ["Fly", "Ride", "Neon", "Mega Neon"]:
        kb.add(InlineKeyboardButton(mod, callback_data=f"trade_mod_{pet_id}_{mod}"))
    await call.message.edit_text(f"Вы выбрали {pet['name']}\nЦена: {pet.get('value','—')}", reply_markup=kb)


@router.callback_query(F.data.startswith("trade_mod_"))
async def apply_trade_mod(call: CallbackQuery):
    parts = call.data.split("_")
    pet_id, mod = parts[2], parts[3]
    pet = ALL_PETS.get(pet_id)
    if not pet:
        await call.answer("Питомец не найден 😢")
        return
    # Сохраняем модификаторы для трейда
    trade_mods = pet.get("trade_mods", set())
    trade_mods.add(mod)
    pet["trade_mods"] = trade_mods
    await call.answer(f"{pet['name']} теперь с модификаторами: {', '.join(trade_mods)}")


# ----------------------
# Авто подсчёт профита/лосса
# ----------------------
@router.message(F.text == "/profit")
async def show_profit(message: Message):
    total_profit = 0
    total_loss = 0
    for pet in ALL_PETS.values():
        value = pet.get("value", 0)
        trade_mods = pet.get("trade_mods", set())
        # Примерная логика подсчёта: каждый модификатор +10%
        value_mod = value
        for mod in trade_mods:
            value_mod *= 1.1
        total_profit += value_mod
        total_loss += value  # без модификаторов
    await message.answer(f"💰 Total Profit: {total_profit}\n📉 Total Loss: {total_loss}")
