import discord
from discord.ext import commands
from bot.loader import load_extensions
from bot.config import TOKEN, INTENTS


bot = commands.Bot(command_prefix="!", intents=INTENTS)


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
