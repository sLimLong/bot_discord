import os
from dotenv import load_dotenv

load_dotenv()

SERVERS = {
    1: {
        "url": os.getenv("SERVER1_URL"),
        "tokenname": os.getenv("SERVER1_TOKENNAME"),
        "secret": os.getenv("SERVER1_SECRET"),

        "telnet_host": os.getenv("SERVER1_TELNET_HOST"),
        "telnet_port": int(os.getenv("SERVER1_TELNET_PORT")),
        "telnet_password": os.getenv("SERVER1_TELNET_PASSWORD"),
    },
    2: {
        "url": os.getenv("SERVER2_URL"),
        "tokenname": os.getenv("SERVER2_TOKENNAME"),
        "secret": os.getenv("SERVER2_SECRET"),

        "telnet_host": os.getenv("SERVER2_TELNET_HOST"),
        "telnet_port": int(os.getenv("SERVER2_TELNET_PORT")),
        "telnet_password": os.getenv("SERVER2_TELNET_PASSWORD"),
    }
}
