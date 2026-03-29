import aiohttp
from bs4 import BeautifulSoup
import asyncio

PET_VALUES = {}

async def load_all_pets():
    """Парсим сайт или API Adopt Me и сохраняем значения в PET_VALUES"""
    url = "https://example.com/adoptme-pets"  # замени на реальный источник
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "lxml")
            for pet in soup.select(".pet-item"):
                name = pet.select_one(".pet-name").text.strip().lower()
                value = int(pet.select_one(".pet-value").text.strip())
                PET_VALUES[name] = value

async def get_value(pet_name: str):
    return PET_VALUES.get(pet_name.lower(), 0)
