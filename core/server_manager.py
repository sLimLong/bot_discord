from core.servers import SERVERS
from core.api_client import APIClient
from core.telnet_client import TelnetClient
from core.storage import update_player


def get_clients(server_id: int):
    cfg = SERVERS.get(server_id)
    if not cfg:
        raise ValueError(f"Server {server_id} not found")

    api = APIClient(cfg["url"], cfg["username"], cfg["password"])
    telnet = TelnetClient(cfg["telnet_host"], cfg["telnet_port"], cfg["telnet_password"])

    return api, telnet


async def get_status(server_id: int):
    api, _ = get_clients(server_id)

    data = await api.get_stats()

    game = data["data"]["gameTime"]

    return {
        "days": game["days"],
        "hours": game["hours"],
        "minutes": game["minutes"],
        "players": data["data"]["players"],
        "hostiles": data["data"]["hostiles"],
        "animals": data["data"]["animals"],
        "server_time": data["meta"]["serverTime"]
    }


async def get_all_players(server_id: int):
    api, _ = get_clients(server_id)
    data = await api.get_players()
    players = data["data"]["players"]

    # сохраняем каждого игрока
    for p in players:
        update_player(server_id, p)

    return players


async def get_online_players(server_id: int):
    players = await get_all_players(server_id)
    return [p for p in players if p.get("online")]


def send_command(server_id: int, cmd: str):
    _, telnet = get_clients(server_id)
    return telnet.send(cmd)
