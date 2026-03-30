

import httpx
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
pets_data = []

async def load_all_pets():
    global pets_data
    try:
        async with httpx.AsyncClient(verify=False, timeout=10) as client:
            resp = await client.get("https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page=1")

            if resp.status_code != 200:
                raise Exception(f"HTTP {resp.status_code}")

            data = resp.json()

            # достаём питомцев
            pets_data = data.get("data", [])

            print(f"Загружено питомцев: {len(pets_data)}")

    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")
        pets_data = []
