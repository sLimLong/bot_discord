import discord
from discord.ext import commands
from bot.loader import load_extensions
from bot.config import TOKEN, INTENTS, ADMIN_IDS

bot = commands.Bot(command_prefix="!", intents=INTENTS)

# Загружаем список админов
bot.admin_ids = [int(x) for x in ADMIN_IDS.split(",")]

# Глобальный cooldown
GLOBAL_COOLDOWN = commands.CooldownMapping.from_cooldown(
    1, 5, commands.BucketType.user  # 1 команда каждые 5 секунд
)

@bot.check
async def global_cooldown(ctx):
    # Админы — без КД
    if ctx.author.id in bot.admin_ids:
        return True

    bucket = GLOBAL_COOLDOWN.get_bucket(ctx.message)
    retry_after = bucket.update_rate_limit()

    if retry_after:
        raise commands.CommandOnCooldown(bucket, retry_after)

    return True


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Подожди {error.retry_after:.1f} сек.")
    else:
        raise error


@bot.event
async def on_ready():
    print("=== Discord bot started ===")
    print(f"Logged in as: {bot.user} (ID: {bot.user.id})")
    print("Loading extensions...")

    await load_extensions(bot)

    print("All extensions loaded.")
    print("Bot is ready.")
    print("===========================")


if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN is missing in .env")
        exit(1)

    bot.run(TOKEN)
