from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import aiohttp

router = Router()

ALL_PETS = []

API_URL = "https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page="


async def load_all_pets():
    global ALL_PETS
    ALL_PETS.clear()

    url = "https://adoptmevalues.gg/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com"
    }

    import aiohttp
    from bs4 import BeautifulSoup

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print("Ошибка при загрузке питомцев:", resp.status)
                    return

                html = await resp.text()

        soup = BeautifulSoup(html, "lxml")

        cards = soup.select("div.card")

        for card in cards:
            name = card.select_one("h3")
            value = card.select_one("span")

            if name:
                ALL_PETS.append({
                    "name": name.text.strip(),
                    "value": value.text.strip() if value else "?"
                })

        print(f"Загружено питомцев: {len(ALL_PETS)}")

    except Exception as e:
        print("Ошибка при загрузке питомцев:", e)
