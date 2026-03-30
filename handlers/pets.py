# handlers/pets.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import httpx

router = Router()
pets_list = []

async def load_all_pets():
    global pets_list
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://example.com/api/pets", timeout=10)
            if resp.status_code != 200 or "application/json" not in resp.headers.get("content-type", ""):
                raise ValueError(f"{resp.status_code}, unexpected mimetype")
            pets_list = resp.json()
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")
        pets_list = []

@router.message(Command("pets"))
async def cmd_pets(message: Message):
    if not pets_list:
        await message.answer("Питомцы пока не загружены 😢")
        return

    kb = InlineKeyboardMarkup(row_width=2)
    for pet in pets_list[:10]:  # первые 10 питомцев
        kb.add(InlineKeyboardButton(text=pet["name"], callback_data=f"pet_{pet['id']}"))
    await message.answer("Список питомцев:", reply_markup=kb)
