from aiogram import Router, types
from aiogram.filters import Command
import asyncio
import httpx

router = Router()

ALL_PETS = []

API_URL = "https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page={page}"

async def fetch_pets():
    page = 1
    pets = []
    async with httpx.AsyncClient(timeout=10) as client:
        while True:
            url = API_URL.format(page=page)
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"Ошибка при загрузке питомцев: {e}")
                break
            if not data.get("data"):
                break
            pets.extend(data["data"])
            page += 1
    return pets

async def load_all_pets():
    global ALL_PETS
    ALL_PETS = await fetch_pets()
    print(f"Загружено питомцев: {len(ALL_PETS)}")

# Команда /pets
@router.message(Command("pets"))
async def show_pets(message: types.Message):
    if not ALL_PETS:
        await message.answer("Питомцы ещё не загружены, попробуйте чуть позже.")
        return
    text = "Все питомцы:\n" + "\n".join([pet["name"] for pet in ALL_PETS])
    await message.answer(text)

# Можно добавить пагинацию, избранное, поиск и callback по клику на питомца
@router.callback_query(lambda c: c.data and c.data.startswith("pet_"))
async def show_pet_details(call: types.CallbackQuery):
    pet_id = call.data.split("_")[1]
    pet = next((p for p in ALL_PETS if str(p["id"]) == pet_id), None)
    if not pet:
        await call.message.edit_text("Питомец не найден.")
        return
    text = f"{pet['name']} — {pet.get('rarity', 'неизвестно')}"
    await call.message.edit_text(text)
