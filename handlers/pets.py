import httpx
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

ALL_PETS = []

API_URL = "https://adoptmevalues.gg/api/v1/values"

async def load_all_pets():
    global ALL_PETS
    ALL_PETS = []
    page = 1
    while True:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}?sortBy=position&limit=100&page={page}")
            if resp.headers.get("content-type") != "application/json":
                print(f"Ошибка при загрузке питомцев: {resp.status_code}, unexpected mimetype")
                break
            data = resp.json()
            if not data:
                break
            ALL_PETS.extend(data)
            page += 1
    print(f"Загружено питомцев: {len(ALL_PETS)}")

# Команда /pets
@router.message()
async def pets_command(message: types.Message):
    if not ALL_PETS:
        await message.answer("Питомцы еще не загружены, подождите минуту.")
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    for pet in ALL_PETS[:20]:  # показываем первые 20
        keyboard.add(
            InlineKeyboardButton(text=pet["name"], callback_data=f"pet_{pet['id']}")
        )
    await message.answer("Выберите питомца:", reply_markup=keyboard)

# Обработка клика на питомца
@router.callback_query(lambda c: c.data and c.data.startswith("pet_"))
async def pet_callback(query: types.CallbackQuery):
    pet_id = query.data.split("_")[1]
    pet = next((p for p in ALL_PETS if str(p["id"]) == pet_id), None)
    if not pet:
        await query.message.edit_text("Питомец не найден.")
        return
    text = f"🐾 {pet['name']}\n💎 Цена: {pet.get('price', 'неизвестно')}"
    await query.message.edit_text(text)
