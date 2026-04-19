import discord
from discord.ext import commands
from core.server_manager import get_online_players

async def setup(bot):
    @bot.command(name="online")
    async def online_cmd(ctx, server_id: int = 1):
        try:
            players = await get_online_players(server_id)

            if not players:
                await ctx.send(f"👥 На сервере {server_id} сейчас никого нет.")
                return

            embed = discord.Embed(
                title=f"Онлайн игроки — Сервер {server_id}",
                color=discord.Color.green()
            )

            for p in players:
                name = p.get("name", "Unknown")
                level = p.get("level", "—")
                ping = p.get("ping", "—")
                health = p.get("health", "—")
                stamina = p.get("stamina", "—")
                score = p.get("score", "—")
                deaths = p.get("deaths", "—")
                kills = p.get("kills", 0)

                pos = p.get("position")
                if pos:
                    pos_str = f"X: {pos.get('x'):.1f}, Y: {pos.get('y'):.1f}, Z: {pos.get('z'):.1f}"
                else:
                    pos_str = "—"

                embed.add_field(
                    name=f"{name} (LvL {level})",
                    value=(
                        f"🏹 **Kills:** {kills}\n"
                        f"💀 **Deaths:** {deaths}\n"
                        f"💠 **Score:** {score}\n"
                        f"❤️ **HP:** {health}\n"
                        f"⚡ **Stamina:** {stamina}\n"
                        f"📡 **Ping:** {ping}\n"
                        f"📍 **Pos:** {pos_str}"
                    ),
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
