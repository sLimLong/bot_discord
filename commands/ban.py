from discord.ext import commands
from core.server_manager import send_command
from core.permissions import is_admin
from bot.servers import SERVERS

async def setup(bot):
    @bot.command(name="ban")
    @is_admin()
    async def ban_cmd(ctx, server_id: int, steamid: str, *, reason: str = "No reason"):
        """
        Использование:
        !ban 1 76561198000000000 Читер
        !ban 2 76561198012345678 Оскорбления
        """

        try:
            send_command(server_id, f'ban add {steamid} "{reason}"')
            await ctx.send(
                f"⛔ Игрок **{steamid}** забанен на сервере **{server_id}**.\nПричина: {reason}"
            )
        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
