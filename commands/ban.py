from discord.ext import commands
from core.server_manager import send_command
from core.permissions import is_admin

async def setup(bot):
    @bot.command(name="ban")
    @is_admin()
    async def ban_cmd(ctx, server_id: int, steamid: str, duration: int, time_unit: str, *, reason: str = "No reason"):
        """
        Использование:
        !ban <server_id> <steamid> <duration> <time_unit> <reason>

        Примеры:
        !ban 1 76561198000000000 300 days cheat
        !ban 2 EOS_0002f809edff445b8d5d5c418e96c60a 12 hours test
        !ban 1 76561198000000000 1 years exploit
        """

        # Нормализуем единицу времени
        time_unit = time_unit.lower()

        VALID_UNITS = {"minutes", "minute", "min",
                       "hours", "hour",
                       "days", "day",
                       "weeks", "week",
                       "months", "month",
                       "years", "year"}

        if time_unit not in VALID_UNITS:
            await ctx.send("❌ Неверная единица времени. Используй: minutes/hours/days/weeks/months/years")
            return

        # Команда Telnet
        cmd = f'ban add {steamid} {duration} {time_unit} "{reason}"'

        try:
            await send_command(server_id, cmd)

            await ctx.send(
                f"⛔ Игрок **{steamid}** забанен на сервере **{server_id}**.\n"
                f"Срок: **{duration} {time_unit}**\n"
                f"Причина: {reason}"
            )

        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")

