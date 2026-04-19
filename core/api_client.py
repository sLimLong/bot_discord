import aiohttp
from aiohttp import BasicAuth

class APIClient:
    def __init__(self, url: str, username: str, password: str):
        self.url = url.rstrip("/")
        self.auth = BasicAuth(username, password)

    async def get(self, endpoint: str):
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(
                f"{self.url}/api/{endpoint}",
                headers={"Accept": "application/json"}
            ) as resp:

                if resp.status == 403:
                    raise Exception("403 Forbidden — неправильный логин/пароль API")

                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")

                try:
                    return await resp.json()
                except:
                    text = await resp.text()
                    raise Exception(f"Сервер вернул не JSON: {text}")

    async def get_stats(self):
        return await self.get("serverstats")

    async def get_players(self):
        return await self.get("player")

    async def get_server_info(self):
        return await self.get("serverstats")

