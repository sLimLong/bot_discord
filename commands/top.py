from discord.ext import commands
from core.server_manager import get_all_players

async def setup(bot):
    @bot.command(name="top")
    async def top_cmd(ctx, server_id: int = 1, mode: str = "score"):
        """
        !top 1              → топ по очкам (score)
        !top 1 score        → топ по очкам
        !top 1 level        → топ по уровню
        !top 1 kills        → топ по убийствам
        !top 1 deaths       → топ по смертям
        """

        try:
            players = await get_all_players(server_id)
        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
            return

        if not players:
            await ctx.send(f"❌ Нет данных о игроках на сервере {server_id}.")
            return

        # сортировка по режиму
        if mode == "score":
            players = sorted(players, key=lambda p: p.get("score", 0), reverse=True)
            title = "💰 Общий баланс очков"

        elif mode == "level":
            players = sorted(players, key=lambda p: p.get("level", 0), reverse=True)
            title = "🏆 Топ по уровню"

        elif mode == "kills":
            players = sorted(players, key=lambda p: p.get("kills", 0), reverse=True)
            title = "💀 Топ по убийствам зомби"

        elif mode == "deaths":
            players = sorted(players, key=lambda p: p.get("deaths", 0), reverse=True)
            title = "⚰ Топ по смертям"

        else:
            await ctx.send("❌ Неизвестный режим. Используй: score / level / kills / deaths")
            return

        # берём топ‑10
        top10 = players[:10]

        text = f"**{title} (Server {server_id})**\n\n"

        for i, p in enumerate(top10, start=1):
            text += (
                f"**#{i} — {p.get('name', 'Unknown')}**\n"
                f"💰 Очки: {p.get('score', 0)}\n"
                f"🎮 Уровень: {p.get('level', 0)}\n"
                f"💀 Убийства: {p.get('kills', 0)}\n"
                f"⚰ Смерти: {p.get('deaths', 0)}\n"
                f"-------------------------\n"
            )

        await ctx.send(text)
