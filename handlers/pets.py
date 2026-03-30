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
        "User-Agent": "Mozilla/5.0"
    }

    import aiohttp
    from bs4 import BeautifulSoup

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                html = await resp.text()

        soup = BeautifulSoup(html, "lxml")

        cards = soup.find_all("div", class_="card")

        for card in cards:
            name = card.find("h3")
            value = card.find("span")

            if name:
                ALL_PETS.append({
                    "name": name.text.strip(),
                    "value": value.text.strip() if value else "?"
                })

        print(f"Загружено питомцев: {len(ALL_PETS)}")

    except Exception as e:
        print("Ошибка при загрузке питомцев:", e)
