import aiohttp
from bot.servers import SERVERS
from core.storage import update_player
from core.telnet_client import TelnetClient



# ============================
# API CLIENT
# ============================

class APIClient:
    def __init__(self, url: str, tokenname: str, secret: str):
        self.url = url.rstrip("/")
        self.tokenname = tokenname
        self.secret = secret

    async def _request(self, method: str, endpoint: str, params=None, data=None):
        url = f"{self.url}{endpoint}"

        # Нормализуем endpoint, чтобы избежать 403 из-за пробелов/слэшей
        clean_endpoint = endpoint.split("?")[0].rstrip("/").strip()

        auth_endpoints = {
            "/api/blacklist",
            "/api/addblacklist",
            "/api/removeblacklist",
            "/api/executeconsolecommand",
            "/api/gmsg",
        }

        # Авторизация только для защищённых эндпоинтов
        if clean_endpoint in auth_endpoints:
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
    # API METHODS
    # -----------------------------

    async def get_players(self):
        return await self._request("GET", "/api/player")

    async def get_stats(self):
        return await self._request("GET", "/api/serverstats")

    async def get_blacklist(self):
        return await self._request("GET", "/api/blacklist")

    async def execute(self, cmd: str):
        return await self._request("POST", "/api/executeconsolecommand", data={"command": cmd})


# ============================
# CLIENT CACHE
# ============================

clients = {}

def get_client(server_id: int):
    if server_id not in clients:
        cfg = SERVERS[server_id]
        clients[server_id] = APIClient(
            url=cfg["url"],
            tokenname=cfg["tokenname"],
            secret=cfg["secret"]
        )
    return clients[server_id]


# ============================
# PLAYERS
# ============================

async def get_all_players(server_id: int):
    api = get_client(server_id)
    data = await api.get_players()

    players = data.get("data", {}).get("players", [])
    result = []

    for p in players:
        platform = p.get("platformId") or {}
        kills = p.get("kills") or {}
        banned = p.get("banned") or {}

        player = {
            "entityId": p.get("entityId"),
            "name": p.get("name"),

            "steamid": platform.get("userId"),
            "platform": platform.get("platformId"),

            # platformId как словарь — важно для storage
            "platformId": platform,

            "online": p.get("online", False),
            "ip": p.get("ip"),
            "ping": p.get("ping"),
            "position": p.get("position"),

            "level": p.get("level"),
            "health": p.get("health"),
            "stamina": p.get("stamina"),
            "score": p.get("score"),
            "deaths": p.get("deaths"),

            # kills всегда словарь
            "kills": {
                "zombies": kills.get("zombies", 0),
                "players": kills.get("players", 0)
            },

            "banned": banned.get("banActive", False),
        }

        update_player(server_id, player)
        result.append(player)

    return result


async def get_online_players(server_id: int):
    players = await get_all_players(server_id)
    return [p for p in players if p["online"]]


# ============================
# SERVER STATUS
# ============================

async def get_status(server_id: int):
    api = get_client(server_id)
    data = await api.get_stats()

    stats = data.get("data", {})
    game_time = stats.get("gameTime", {})

    return {
        "players": stats.get("players", 0),
        "hostiles": stats.get("hostiles", 0),
        "animals": stats.get("animals", 0),
        "game_days": game_time.get("days"),
        "game_hours": game_time.get("hours"),
        "game_minutes": game_time.get("minutes"),
    }


# ============================
# BAN LIST
# ============================

async def get_ban_list(server_id: int):
    api = get_client(server_id)
    data = await api.get_blacklist()

    # Формат: {"data": [ {...}, {...} ], "meta": {...}}
    bans = data.get("data", []) if isinstance(data.get("data"), list) else []

    result = []

    for b in bans:
        user = b.get("userId", {})
        result.append({
            "steamid": user.get("userId"),
            "platform": user.get("platformId"),
            "name": b.get("name", ""),
            "reason": b.get("banReason", "—"),
            "until": b.get("bannedUntil"),
        })

    return result


# ============================
# COMMAND EXECUTION
# ============================

async def send_command(server_id: int, cmd: str):
    telnet = get_telnet(server_id)
    return await telnet.send(cmd)

def get_telnet(server_id: int):
    cfg = SERVERS[server_id]
    return TelnetClient(
        host=cfg["telnet_host"],
        port=cfg["telnet_port"],
        password=cfg["telnet_password"]
    )
