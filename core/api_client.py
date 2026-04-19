import aiohttp

class APIClient:
    def __init__(self, url: str, tokenname: str, secret: str):
        self.url = url.rstrip("/")
        self.tokenname = tokenname
        self.secret = secret

        # эндпоинты, которые требуют авторизации
        self.auth_required = {
            "/api/blacklist",
            "/api/addblacklist",
            "/api/removeblacklist",
            "/api/executeconsolecommand",
            "/api/bloodmoon",
            "/api/gmsg",
            "/api/player",
            "/api/serverstats",
        }

    async def _request(self, method: str, endpoint: str, params=None, data=None):
        url = f"{self.url}{endpoint}"

        # Если endpoint требует авторизацию
        if any(endpoint.startswith(ep) for ep in self.auth_required):
            headers = {
                "accept": "application/json",
                "x-sdtd-api-tokenname": self.tokenname,
                "x-sdtd-api-secret": self.secret
            }
        else:
            headers = {"accept": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=10
            ) as resp:

                text = await resp.text()

                if resp.status != 200:
                    raise Exception(f"API error {resp.status}: {text}")

                try:
                    return await resp.json()
                except:
                    return {"raw": text}

    # -----------------------------
    # PUBLIC API METHODS
    # -----------------------------

    async def get(self, endpoint: str):
        return await self._request("GET", endpoint)

    async def post(self, endpoint: str, data=None):
        return await self._request("POST", endpoint, data=data)

    async def get_blacklist(self):
        return await self.get("/api/blacklist")

    async def execute(self, cmd: str):
        return await self.post("/api/executeconsolecommand", data={"command": cmd})

    async def get_stats(self):
        return await self.get("/api/serverstats")

    async def get_players(self):
        return await self.get("/api/player")

    async def get_server_info(self):
        return await self.get("/api/getserverinfo")

    async def get_bloodmoon(self):
        return await self.get("/api/bloodmoon")
