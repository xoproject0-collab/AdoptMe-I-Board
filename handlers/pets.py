# handlers/pets.py
import httpx
import ssl

async def load_all_pets():
    global pets_list
    try:
        # создаем SSL-контекст без проверки сертификата (временно для теста)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with httpx.AsyncClient(verify=ssl_context) as client:
            resp = await client.get("https://example.com/api/pets", timeout=10)
            if resp.status_code != 200 or "application/json" not in resp.headers.get("content-type", ""):
                raise ValueError(f"{resp.status_code}, unexpected mimetype")
            pets_list = resp.json()
    except Exception as e:
        print(f"Ошибка при загрузке питомцев: {e}")
        pets_list = []
