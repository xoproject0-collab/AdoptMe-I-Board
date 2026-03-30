# pets.py
import aiohttp
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_URL = "https://adoptmevalues.gg/api/v1/values"
PAGE_LIMIT = 100  # сколько питомцев за раз загружаем
UPDATE_INTERVAL = 600  # 10 минут
ALL_PETS = {}  # здесь будем хранить всех питомцев

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


async def fetch_page(session, page: int):
    """Загружаем одну страницу питомцев"""
    try:
        async with session.get(f"{API_URL}?sortBy=position&limit={PAGE_LIMIT}&page={page}", headers=headers) as resp:
            if resp.status != 200:
                print(f"Ошибка при загрузке страницы {page}: {resp.status}")
                return []
            try:
                data = await resp.json()
                return data.get("data", [])
            except Exception as e:
                print(f"Ошибка при разборе JSON страницы {page}: {e}")
                return []
    except Exception as e:
        print(f"Ошибка запроса страницы {page}: {e}")
        return []


async def load_all_pets():
    """Загружаем всех питомцев со всех страниц"""
    global ALL_PETS
    ALL_PETS = {}
    page = 1
    async with aiohttp.ClientSession() as session:
        while True:
            pets = await fetch_page(session, page)
            if not pets:
                break  # больше нет страниц
            for pet in pets:
                pet_id = pet.get("id")
                if pet_id:
                    ALL_PETS[pet_id] = pet
            page += 1
        print(f"✅ Загружено питомцев: {len(ALL_PETS)}")


def start_auto_update():
    """Запускаем автообновление каждые 10 минут"""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_all_pets, "interval", seconds=UPDATE_INTERVAL)
    scheduler.start()


# Для старта при импорте
async def init():
    await load_all_pets()
    start_auto_update()


# Пример запуска вручную, если нужно для теста
if __name__ == "__main__":
    asyncio.run(init())
