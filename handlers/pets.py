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

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    page = 1

    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            url = API_URL + str(page)

            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print(f"Ошибка загрузки: HTTP {resp.status}")
                        break

                    data = await resp.json()
                    pets = data.get("data", [])

                    if not pets:
                        break

                    ALL_PETS.extend(pets)
                    print(f"Страница {page} загружена ({len(pets)})")

                    page += 1

            except Exception as e:
                print("Ошибка при загрузке питомцев:", e)
                break

    print(f"Всего питомцев: {len(ALL_PETS)}")


@router.message(Command("pets"))
async def pets_command(message: Message):
    if not ALL_PETS:
        await message.answer("❌ Питомцы не загружены")
        return

    text = "🐾 Список питомцев:\n\n"

    for pet in ALL_PETS[:20]:
        text += f"• {pet.get('name')} ({pet.get('value', '?')})\n"

    text += "\n...и еще много"

    await message.answer(text)
