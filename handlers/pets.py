import httpx
import asyncio

ALL_PETS = []

API_URL = "https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page=1"

async def load_all_pets():
    global ALL_PETS
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(API_URL, headers={"Accept": "application/json"})
            if resp.status_code == 200 and "application/json" in resp.headers.get("Content-Type", ""):
                data = resp.json()
                ALL_PETS = [{"name": p["name"], "value": p.get("value", 0)} for p in data]
                print(f"Загружено питомцев: {len(ALL_PETS)}")
            else:
                print(f"Ошибка при загрузке питомцев: {resp.status_code}, {resp.headers.get('Content-Type')}")
                ALL_PETS = []
    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка при загрузке питомцев: {e}")
        ALL_PETS = []
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")
        ALL_PETS = []
