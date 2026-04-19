from discord.ext import commands
from core.server_manager import get_status

async def setup(bot):
    @bot.command(name="status")
    async def status_cmd(ctx, server_id: int = 1):
        try:
            s = await get_status(server_id)
        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
            return

        text = (
            f"📡 **Статус сервера {server_id}**\n"
            f"🕒 Игровое время: {s['days']} дн., {s['hours']:02d}:{s['minutes']:02d}\n"
            f"👥 Игроков онлайн: {s['players']}\n"
            f"👹 Враги: {s['hostiles']}\n"
            f"🐺 Животные: {s['animals']}\n"
            f"⏱ Серверное время: {s['server_time']}\n"
        )

        await ctx.send(text)
