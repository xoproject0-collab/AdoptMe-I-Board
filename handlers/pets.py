import httpx
import certifi

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command   # ← ВОТ ЭТА СТРОКА ОБЯЗАТЕЛЬНА

router = Router()
pets_data = []

async def load_all_pets():
    global pets_data
    try:
        async with httpx.AsyncClient(verify=certifi.where(), timeout=10) as client:
            resp = await client.get("https://example.com/api/pets")
            resp.raise_for_status()
            pets_data = resp.json()
            print(f"Загружено питомцев: {len(pets_data)}")
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")

@router.message(Command("pets"))
async def cmd_pets(message: Message):
    if not pets_data:
        await message.answer("Питомцы пока не загружены 😢")
        return
    text = "Список питомцев:\n" + "\n".join(f"{p['name']} - {p['type']}" for p in pets_data)
    await message.answer(text)
