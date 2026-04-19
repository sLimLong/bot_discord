import json
import os
from datetime import datetime

DATA_DIR = "data"


def ensure_dir():
    """Создаёт папку data/, если её нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_file(server_id: int):
    """Возвращает путь к JSON-файлу сервера."""
    ensure_dir()
    return os.path.join(DATA_DIR, f"server_{server_id}_players.json")


def load_data(server_id: int):
    """Загружает JSON. Если файл пустой или битый — возвращает пустую структуру."""
    path = get_file(server_id)

    if not os.path.exists(path):
        return {"players": {}}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # файл пустой → возвращаем пустую структуру
            if not content:
                return {"players": {}}

            return json.loads(content)

    except Exception:
        # файл битый → пересоздаём
        return {"players": {}}


def save_data(server_id: int, data: dict):
    """Сохраняет JSON."""
    path = get_file(server_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_player(server_id: int, player: dict):
    """
    Обновляет данные игрока в JSON.
    Вызывается при каждом запросе get_all_players().
    """
    data = load_data(server_id)

    steam = player["platformId"]["userId"]

    data["players"][steam] = {
        "name": player["name"],
        "score": player["score"],
        "level": player["level"],
        "kills": player["kills"]["zombies"],
        "deaths": player["deaths"],
        "last_update": datetime.now().isoformat()
    }

    save_data(server_id, data)
