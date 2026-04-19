import discord
from discord.ext import commands
from core.server_manager import get_status

async def setup(bot):
    @bot.command(name="status")
    async def status_cmd(ctx, server_id: int = 1):
        try:
            status = await get_status(server_id)

            # Если сервер не ответил
            if not status or status.get("players") is None:
                await ctx.send(f"❌ Сервер #{server_id} сейчас **OFFLINE** или не отвечает.")
                return

            embed = discord.Embed(
                title=f"📡 Статус сервера #{server_id}",
                color=discord.Color.green()
            )
            embed.add_field(
                name="🌎 Флора сервера\n",
                value=(
                    f"-------------------------------------\n"
                    f"👥 Игроки онлайн: {status['players']}\n"
                    f"-------------------------------------\n"
                    f"🐺 Животные: {status['animals']}\n"
                    f"-------------------------------------\n"
                    f"💀 Зомби: {status['hostiles']}\n"
                    f"-------------------------------------\n"                    
                ),
                inline=False
            )            

            # Игровое время
            embed.add_field(
                name="⏳ Игровое время\n",
                value=(
                    f"-------------------------------------\n"
                    f"📅 Дни: {status['game_days']}\n"
                    f"-------------------------------------\n"
                    f"🕒 Время: {status['game_hours']}:{status['game_minutes']}\n"
                ),
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception:
            await ctx.send(f"❌ Сервер #{server_id} сейчас **OFFLINE** или не отвечает.")
