import os
from dotenv import load_dotenv

load_dotenv()

SERVERS = {
    1: {
        "url": os.getenv("SERVER1_URL"),
        "tokenname": os.getenv("SERVER1_TOKENNAME"),
        "secret": os.getenv("SERVER1_SECRET"),
    },
    2: {
        "url": os.getenv("SERVER2_URL"),
        "tokenname": os.getenv("SERVER2_TOKENNAME"),
        "secret": os.getenv("SERVER2_SECRET"),
    }
}
