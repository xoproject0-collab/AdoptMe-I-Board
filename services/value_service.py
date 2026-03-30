import aiohttp
from bs4 import BeautifulSoup

ALL_PETS = []

URL = "https://adoptmevalues.gg/calculator"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

async def load_all_pets():
    global ALL_PETS
    ALL_PETS = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(URL) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")

    cards = soup.select("div.item-card")  # может отличаться

    for card in cards:
        try:
            name = card.select_one(".item-name").text.strip()
            value = card.select_one(".item-value").text.strip()

            ALL_PETS.append({
                "name": name,
                "value": value
            })
        except:
            continue

    print(f"Загружено питомцев: {len(ALL_PETS)}")
