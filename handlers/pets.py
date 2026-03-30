import httpx
from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

PETS_API_URL = "https://example.com/api/pets"

pets_list = []

async def load_all_pets():
    global pets_list
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(PETS_API_URL, timeout=10)
            if resp.status_code != 200 or resp.headers.get("content-type") != "application/json":
                raise ValueError(f"{resp.status_code}, unexpected mimetype")
            pets_list = resp.json()
            print(f"Загружено питомцев: {len(pets_list)}")
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")
        pets_list = []

# Пример команды /pets
@router.message(commands=["pets"])
async def cmd_pets(message: Message):
    if not pets_list:
        await message.answer("Питомцы пока не загружены 😢")
        return

    kb = InlineKeyboardMarkup(row_width=2)
    for pet in pets_list[:10]:  # показываем первые 10
        kb.add(InlineKeyboardButton(text=pet["name"], callback_data=f"pet_{pet['id']}"))
    await message.answer("Список питомцев:", reply_markup=kb)
