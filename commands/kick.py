from discord.ext import commands
from core.server_manager import send_command
from core.permissions import is_admin

async def setup(bot):
    @bot.command(name="kick")
    @is_admin()
    async def kick_cmd(ctx, server_id: int, player: str, *, reason: str = "No reason"):
        """
        Использование:
        !kick 1 RAY Нарушение правил
        !kick 2 .:BenThrottle:. Читер
        """

        try:
            send_command(server_id, f'kick {player} "{reason}"')
            await ctx.send(f"👢 Игрок **{player}** кикнут с сервера **{server_id}**.\nПричина: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
