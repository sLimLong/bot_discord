import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Загружаем ID админов из .env
# Пример в .env:
# ADMIN_IDS=123456789012345678,987654321012345678
ADMIN_IDS = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x) for x in ADMIN_IDS.split(",") if x.strip().isdigit()]


def is_admin():
    async def predicate(ctx: commands.Context):
        user = ctx.author

        # Проверка по ID
        if user.id in ADMIN_IDS:
            return True

        await ctx.send("❌ У вас нет прав для выполнения этой команды.")
        return False

    return commands.check(predicate)
