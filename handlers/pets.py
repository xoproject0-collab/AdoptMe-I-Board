# pets.py
import aiohttp
import asyncio
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

API_URL = "https://adoptmevalues.gg/api/v1/values"
all_pets = []  # глобально храним всех питомцев

# --------------------------
# Загрузка всех питомцев
# --------------------------
async def fetch_page(session, page, limit=100):
    params = {"sortBy": "position", "limit": limit, "page": page}
    async with session.get(API_URL, params=params) as resp:
        if resp.content_type != "application/json":
            raise ValueError(f"Unexpected mimetype: {resp.content_type}")
        return await resp.json()

async def load_all_pets():
    global all_pets
    all_pets = []
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            data = await fetch_page(session, page)
            pets_page = data.get("data", [])
            if not pets_page:
                break
            all_pets.extend(pets_page)
            page += 1
    print(f"✅ Загружено питомцев: {len(all_pets)}")

# --------------------------
# Клавиатура питомцев (страницы + inline)
# --------------------------
def build_pets_keyboard(page=0, per_page=10):
    kb = InlineKeyboardMarkup(row_width=2)
    start = page * per_page
    end = start + per_page
    for pet in all_pets[start:end]:
        name = pet["name"]
        kb.add(InlineKeyboardButton(text=name, callback_data=f"pet_{name}"))
    # Страницы
    if start > 0:
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page-1}"))
    if end < len(all_pets):
        kb.add(InlineKeyboardButton("➡️ Вперед", callback_data=f"page_{page+1}"))
    return kb

# --------------------------
# Inline кнопки и поиск
# --------------------------
@router.message(commands=["pets"])
async def show_pets(message: types.Message):
    kb = build_pets_keyboard(page=0)
    await message.answer("Список питомцев:", reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("page_"))
async def paginate_pets(call: types.CallbackQuery):
    page = int(call.data.split("_")[1])
    kb = build_pets_keyboard(page=page)
    await call.message.edit_reply_markup(kb)

@router.message()
async def search_pet(message: types.Message):
    query = message.text.lower()
    results = [pet for pet in all_pets if query in pet["name"].lower()]
    if not results:
        await message.answer("Питомец не найден 😢")
        return
    kb = InlineKeyboardMarkup(row_width=2)
    for pet in results[:10]:
        kb.add(InlineKeyboardButton(text=pet["name"], callback_data=f"pet_{pet['name']}"))
    await message.answer(f"Результаты поиска для: {query}", reply_markup=kb)

# --------------------------
# Детали питомца и модификаторы
# --------------------------
@router.callback_query(lambda c: c.data and c.data.startswith("pet_"))
async def show_pet_details(call: types.CallbackQuery):
    name = call.data.split("_", 1)[1]
    pet = next((p for p in all_pets if p["name"] == name), None)
    if not pet:
        await call.message.answer("Ошибка: питомец не найден")
        return

    # Строим текст с модификаторами
    modifiers = []
    for mod in ["fly", "ride", "neon", "megaNeon"]:
        if pet.get(mod):
            modifiers.append(mod.capitalize())
    mods_text = " | ".join(modifiers) if modifiers else "Нет модификаторов"

    text = f"🐾 <b>{pet['name']}</b>\n💰 Цена: {pet.get('value', 0)}\n🔧 Модификаторы: {mods_text}"
    await call.message.answer(text)
