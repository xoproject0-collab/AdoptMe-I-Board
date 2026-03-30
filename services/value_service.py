import json
import aiohttp
import asyncio

PETS_FILE = "data/pets.json"

async def fetch_all_pets():
    """Загружаем всех питомцев со всех страниц API"""
    pets = []
    page = 1
    limit = 100  # больше за один запрос
    async with aiohttp.ClientSession() as session:
        while True:
            url = f"https://adoptmevalues.gg/api/v1/values?sortBy=position&limit={limit}&page={page}"
            async with session.get(url) as resp:
                data = await resp.json()
                if not data["results"]:
                    break
                pets.extend(data["results"])
                page += 1
    # Сохраняем локально
    with open(PETS_FILE, "w", encoding="utf-8") as f:
        json.dump(pets, f, ensure_ascii=False, indent=2)
    return pets

async def load_all_pets():
    """Обновляем всех питомцев"""
    try:
        return await fetch_all_pets()
    except Exception as e:
        print("Ошибка при загрузке питомцев:", e)
        return []

async def get_pets():
    """Возвращаем питомцев из локального файла"""
    try:
        with open(PETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return await load_all_pets()
