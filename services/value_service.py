import aiohttp
import asyncio

# Словарь всех питомцев и их value
pets = {}
pet_list = []

async def load_all_pets():
    """Загружает всех питомцев с публичного источника Adopt Me"""
    global pets, pet_list
    url = "https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=500&page=1"  # публичный доступ

    new_values = {}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers={"User-Agent": "AdoptMeBot/1.0"}) as r:
                if r.status != 200:
                    text = await r.text()
                    print(f"[ERROR] Status: {r.status}, response: {text}")
                    return
                data = await r.json(content_type=None)
        except Exception as e:
            print(f"[ERROR] Ошибка при запросе: {e}")
            return

    items = data.get("values", [])
    for pet in items:
        name = pet.get("name", "").lower()
        value = pet.get("value", 0)
        new_values[name] = value

    pets.update(new_values)
    pet_list.clear()
    pet_list.extend(new_values.keys())

    print(f"[INFO] Загружено питомцев: {len(pets)}")

def get_value(name: str) -> int:
    """Получить value питомца по имени"""
    return pets.get(name.lower(), 0)

def search_pet(text: str) -> list[str]:
    """Поиск питомцев по подстроке"""
    results = [p for p in pet_list if text.lower() in p]
    return results[:10]

def calculate_trade_value(pets_in_trade: list[dict]) -> int:
    """Суммируем value всех питомцев в трейде"""
    return sum(get_value(p["name"]) for p in pets_in_trade)
