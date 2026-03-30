import aiohttp
import json
from pathlib import Path

DATA_FILE = Path("data/pets.json")

ALL_PETS = {}

async def load_all_pets():
    global ALL_PETS
    url = "https://adoptmevalues.gg/data.json"  # пример, нужно реальный API или парсер
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    pets = {}
    for pet in data["pets"]:  # структура зависит от API сайта
        category = pet["rarity"].lower()
        pets.setdefault(category, []).append({
            "name": pet["name"],
            "value": pet["value"]
        })

    ALL_PETS = pets
    # сохраняем кэш
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(pets, ensure_ascii=False))
