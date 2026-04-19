import discord
from discord.ext import commands
from core.api_client import APIClient
from bot.servers import SERVERS
from datetime import datetime, timedelta
import pytz


async def setup(bot):
    @bot.command(name="bloodmoon")
    async def bloodmoon_cmd(ctx, server_id: int = 1):
        """
        Показывает информацию о следующей кровавой луне через Alloc API.
        """

        # Проверяем, есть ли сервер
        if server_id not in SERVERS:
            await ctx.send("❌ Сервер с таким ID не найден.")
            return

        server = SERVERS[server_id]

        # Создаём API клиент
        client = APIClient(
            url=server["url"],
            tokenname=server["tokenname"],
            secret=server["secret"]
        )

        # Запрашиваем /api/bloodmoon
        try:
            response = await client.get("/api/bloodmoon")
        except Exception as e:
            await ctx.send(f"❌ Ошибка API: {e}")
            return

        # Проверяем корректность ответа
        if (
            not response
            or "data" not in response
            or "nextBloodmoon" not in response["data"]
            or "gameTime" not in response["data"]
            or "meta" not in response
            or "serverTime" not in response["meta"]
        ):
            await ctx.send("❌ API вернул некорректный ответ. Возможно, сервер оффлайн или авторизация неверна.")
            return

        data = response["data"]
        meta = response["meta"]

        # Текущее игровое время
        game = data["gameTime"]
        cur_day = game["days"]
        cur_hour = game["hours"]
        cur_minute = game["minutes"]

        # Следующий Blood Moon
        next_bm = data["nextBloodmoon"]
        bm_day = next_bm["days"]
        bm_hour = next_bm["hours"]
        bm_minute = next_bm["minutes"]

        # Реальное время сервера
        server_time = datetime.fromisoformat(meta["serverTime"])

        # === Конвертация игрового времени в реальное ===
        # 1 игровой день = 120 минут реального времени
        # 1 игровой час = 5 минут реального времени
        # 1 игровая минута = 5 секунд реального времени

        total_game_minutes_left = (
            (bm_day - cur_day) * 24 * 60 +
            (bm_hour - cur_hour) * 60 +
            (bm_minute - cur_minute)
        )

        real_seconds_left = total_game_minutes_left * 5

        # Реальное время КН
        bm_real_time = server_time + timedelta(seconds=real_seconds_left)

        # Перевод в МСК
        msk = pytz.timezone("Europe/Moscow")
        bm_msk = bm_real_time.astimezone(msk)

        # === Формируем embed ===
        embed = discord.Embed(
            title="🌕 Следующая Кровавая Луна",
            color=discord.Color.red()
        )

        embed.add_field(name="Текущий игровой день", value=str(cur_day), inline=True)
        embed.add_field(name="День КН", value=str(bm_day), inline=True)

        embed.add_field(
            name="До КН (игровое время)",
            value=f"{bm_day - cur_day} дн, {bm_hour - cur_hour} ч, {bm_minute - cur_minute} мин",
            inline=False
        )

        embed.add_field(
            name="Реальное время КН (МСК)",
            value=bm_msk.strftime("%Y-%m-%d %H:%M:%S"),
            inline=False
        )

        await ctx.send(embed=embed)
