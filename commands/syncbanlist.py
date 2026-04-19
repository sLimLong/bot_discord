import os
import discord
from discord.ext import commands
from core.server_manager import get_ban_list, send_command
from core.permissions import is_admin
from core.ban_log import add_ban, load_bans
from dotenv import load_dotenv
from bot.servers import SERVERS

load_dotenv()
BAN_LOG_CHANNEL = int(os.getenv("BAN_LOG_CHANNEL", 0))


async def setup(bot):
    @bot.command(name="syncbanlist")
    @is_admin()
    async def sync_ban_list(ctx):
        await ctx.send("🔄 Получаю бан‑лист с серверов...")

        # Локальный JSON
        local = load_bans()
        local_bans = {b["steamid"] for b in local["bans"]}

        # Получаем баны с серверов
        bans_s1 = await get_ban_list(1)
        bans_s2 = await get_ban_list(2)

        # Объединяем
        all_bans = {}

        for b in bans_s1:
            all_bans[b["steamid"]] = b["reason"]

        for b in bans_s2:
            all_bans[b["steamid"]] = b["reason"]

        synced = 0

        for steamid, reason in all_bans.items():

            # Новый бан?
            if steamid not in local_bans:
                entry = add_ban(
                    steamid=steamid,
                    reason=reason,
                    admin="SYNC",
                    server_id=0
                )

                # Embed в канал
                if BAN_LOG_CHANNEL:
                    channel = bot.get_channel(BAN_LOG_CHANNEL)
                    if channel:
                        embed = discord.Embed(
                            title="🔄 Синхронизирован бан",
                            color=discord.Color.orange()
                        )
                        embed.add_field(name="SteamID", value=steamid, inline=False)
                        embed.add_field(name="Причина", value=reason, inline=False)
                        embed.add_field(name="Источник", value="Серверы 1+2", inline=False)
                        embed.set_footer(text=f"Время: {entry['timestamp']}")
                        await channel.send(embed=embed)

                synced += 1

            # Применяем бан на обоих серверах
            await send_command(1, f'ban add {steamid} "{reason}"')
            await send_command(2, f'ban add {steamid} "{reason}"')

        await ctx.send(f"✅ Синхронизация завершена. Новых банов: **{synced}**.")
