import asyncio
import httpx

URL = "http://localhost:8000/api/v1/strategies/state"  # Подставьте ваш URL эндпоинта
headers={"X-UID": "8698", "X-Token": "tBY9b3YrfJkDA4P"}

async def make_request():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, headers=headers)
        print(response.json())
    await asyncio.sleep(0.1)


async def main():
    tasks = [make_request() for _ in range(1000)]  # Много одновременных запросов
    await asyncio.gather(*tasks)

asyncio.run(main())