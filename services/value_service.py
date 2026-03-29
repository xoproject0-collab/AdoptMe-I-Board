import aiohttp
from config import TOKEN

pets = {}
pet_list = []

async def load_all_pets():
    global pets, pet_list
    page = 1
    new_values = {}
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "AdoptMeBot/1.0"
    }

    async with aiohttp.ClientSession() as session:
        while True:
            url = f"https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page={page}"
            async with session.get(url, headers=headers) as r:
                if r.status != 200:
                    text = await r.text()
                    print(f"[ERROR] Status: {r.status}, response: {text}")
                    break
                data = await r.json(content_type=None)
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
    return pets.get(name.lower(), 0)

def search_pet(text):
    results = [p for p in pet_list if text.lower() in p]
    return results[:10]
