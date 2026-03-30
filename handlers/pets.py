# pets.py
import aiohttp
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()  # 🔹 создаём router для include_router

API_URL = "https://adoptmevalues.gg/api/v1/values"
PAGE_LIMIT = 100
UPDATE_INTERVAL = 600  # 10 минут
ALL_PETS = {}  # сюда будем складывать всех питомцев
FAVORITES = {}  # избранное: user_id -> list of pet_ids

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


async def fetch_page(session, page: int):
    try:
        async with session.get(f"{API_URL}?sortBy=position&limit={PAGE_LIMIT}&page={page}", headers=headers) as resp:
            if resp.status != 200:
                print(f"Ошибка при загрузке страницы {page}: {resp.status}")
                return []
            try:
                data = await resp.json()
                return data.get("data", [])
            except Exception as e:
                print(f"Ошибка JSON страницы {page}: {e}")
                return []
    except Exception as e:
        print(f"Ошибка запроса страницы {page}: {e}")
        return []


async def load_all_pets():
    global ALL_PETS
    ALL_PETS = {}
    page = 1
    async with aiohttp.ClientSession() as session:
        while True:
            pets = await fetch_page(session, page)
            if not pets:
                break
            for pet in pets:
                pet_id = pet.get("id")
                if pet_id:
                    ALL_PETS[pet_id] = pet
            page += 1
    print(f"✅ Загружено питомцев: {len(ALL_PETS)}")


def start_auto_update():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", seconds=UPDATE_INTERVAL)
    scheduler.start()


# ----------------------
# 🔹 Хэндлеры для бота
# ----------------------

@router.message(F.text == "/pets")
async def show_first_page(message: Message):
    """Показываем первую страницу питомцев"""
    if not ALL_PETS:
        await message.answer("Питомцы ещё загружаются, подождите...")
        return
    pets_list = list(ALL_PETS.values())[:10]  # первая страница
    kb = InlineKeyboardMarkup(row_width=2)
    for pet in pets_list:
        kb.add(InlineKeyboardButton(pet["name"], callback_data=f"pet_{pet['id']}"))
    await message.answer("Питомцы (страница 1):", reply_markup=kb)


@router.callback_query(F.data.startswith("pet_"))
async def show_pet_page(call: CallbackQuery):
    pet_id = call.data.split("_")[1]
    pet = ALL_PETS.get(pet_id)
    if not pet:
        await call.message.edit_text("Питомец не найден 😢")
        return
    # Кнопки модификаторов
    kb = InlineKeyboardMarkup(row_width=2)
    for mod in ["Fly", "Ride", "Neon", "Mega Neon"]:
        kb.add(InlineKeyboardButton(mod, callback_data=f"mod_{pet_id}_{mod}"))
    kb.add(InlineKeyboardButton("❤️ В избранное", callback_data=f"fav_{pet_id}"))
    await call.message.edit_text(f"🐾 {pet['name']}\nЦена: {pet.get('value', '—')}", reply_markup=kb)


@router.callback_query(F.data.startswith("fav_"))
async def add_to_favorites(call: CallbackQuery):
    user_id = call.from_user.id
    pet_id = call.data.split("_")[1]
    FAVORITES.setdefault(user_id, set()).add(pet_id)
    await call.answer("Добавлено в избранное ❤️")


@router.callback_query(F.data.startswith("mod_"))
async def apply_modifier(call: CallbackQuery):
    parts = call.data.split("_")
    pet_id, mod = parts[1], parts[2]
    pet = ALL_PETS.get(pet_id)
    if not pet:
        await call.answer("Питомец не найден 😢")
        return
    # Логика комбинирования модификаторов
    mods = pet.get("mods", set())
    mods.add(mod)
    pet["mods"] = mods
    await call.answer(f"{pet['name']} теперь с модификаторами: {', '.join(mods)}")


# ----------------------
# 🔹 Инициализация при старте
# ----------------------
async def init():
    await load_all_pets()
    start_auto_update()
