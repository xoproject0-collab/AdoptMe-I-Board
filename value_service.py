import aiohttp
import asyncio

# Словарь всех питомцев и их value
pets = {}
pet_list = []

async def load_all_pets():
    """Загружает всех питомцев с сайта Adopt Me"""
    global pets, pet_list
    page = 1
    new_values = {}
    async with aiohttp.ClientSession() as session:
        while True:
            url = f"https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page={page}"
            async with session.get(url) as r:
                data = await r.json()
            items = data.get("values", [])
            if not items:
                break
            for pet in items:
                name = pet["name"]
                value = pet["value"]
                new_values[name.lower()] = value
            page += 1
    pets = new_values
    pet_list = list(new_values.keys())
    print(f"[INFO] Загружено питомцев: {len(pets)}")

def get_value(name):
    """Получить value питомца по имени"""
    return pets.get(name.lower(), 0)

def search_pet(text):
    """Поиск питомцев по подстроке"""
    results = [p for p in pet_list if text.lower() in p]
    return results[:10]