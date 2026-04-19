import json
import os
from datetime import datetime

DATA_DIR = "data"
BAN_FILE = os.path.join(DATA_DIR, "ban_list.json")


def ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_bans():
    ensure_dir()
    if not os.path.exists(BAN_FILE):
        return {"bans": []}

    try:
        with open(BAN_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {"bans": []}
            return json.loads(content)
    except:
        return {"bans": []}


def save_bans(data):
    ensure_dir()
    with open(BAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_ban(steamid, reason, admin, server_id):
    data = load_bans()

    entry = {
        "steamid": steamid,
        "reason": reason,
        "admin": admin,
        "server_id": server_id,
        "timestamp": datetime.now().isoformat()
    }

    data["bans"].append(entry)
    save_bans(data)

    return entry
