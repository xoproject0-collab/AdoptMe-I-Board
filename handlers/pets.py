import aiohttp

ALL_PETS = []

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://adoptmevalues.gg/"
}

async def load_all_pets():
    global ALL_PETS
    ALL_PETS = []

    page = 1

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            url = f"https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=50&page={page}"

            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print(f"Ошибка: {resp.status}")
                        break

                    data = await resp.json(content_type=None)

                    items = data.get("data", [])
                    if not items:
                        break

                    for pet in items:
                        ALL_PETS.append({
                            "name": pet.get("name"),
                            "value": pet.get("value", 0),
                            "rarity": pet.get("rarity", "unknown")
                        })

                    print(f"Загружена страница {page}")
                    page += 1

            except Exception as e:
                print("Ошибка при загрузке питомцев:", e)
                break

    print(f"Всего питомцев: {len(ALL_PETS)}")
