"""
Есть список URL (1000 штук).
Нужно написать функцию, которая:
Делает асинхронные HTTP-запросы по всем URL.
Одновременно выполняет не больше N запросов.
Возвращает результаты в том же порядке, что и входящие URL.
Корректно обрабатывает ошибки (запрос упал → вернуть None).
"""

import asyncio
import aiohttp


async def fetch_one(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                return None
        except Exception:
            return None


async def fetch_all(urls: list[str], limit: int = 10) -> list[str | None]:
    sem = asyncio.Semaphore(limit)

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_one(session, url, sem))
            for url in urls
        ]

        # gather сохраняет порядок!
        results = await asyncio.gather(*tasks)
        return results


if __name__ == '__main__':
    asyncio.run(fetch_all(["https://httpbin.org/get"]))