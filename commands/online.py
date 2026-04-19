from discord.ext import commands
from core.server_manager import get_online_players

async def setup(bot):
    @bot.command(name="online")
    async def online_cmd(ctx, server_id: int = 1):
        try:
            players = await get_online_players(server_id)
        except Exception as e:
            await ctx.send(f"❌ Ошибка: {e}")
            return

        if not players:
            await ctx.send(f"👥 На сервере {server_id} сейчас никого нет.")
            return

        text = f"👥 **Онлайн на сервере {server_id}: {len(players)} игрок(ов)**\n\n"

        for p in players:
            name = p["name"]
            level = p["level"]
            ping = p["ping"]
            steam = p["platformId"]["userId"]
            hp = p["health"]
            stamina = int(p["stamina"])
            zkills = p["kills"]["zombies"]
            deaths = p["deaths"]

            text += (
                f"**{name}** (Lv {level})\n"
                f"🏃 HP: {hp} | STA: {stamina}\n"
                f"🔫 ZKills: {zkills} | 💀 Deaths: {deaths}\n"
                f"📡 Ping: {ping} | SteamID: `{steam}`\n"
                f"-------------------------\n"
            )

        await ctx.send(text)
