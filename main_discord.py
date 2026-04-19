import discord
from discord.ext import commands
from bot.loader import load_extensions
from bot.config import TOKEN, INTENTS


bot = commands.Bot(command_prefix="!", intents=INTENTS)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")
    print("Loading extensions...")
    load_extensions(bot)
    print("Bot is ready.")


def run():
    bot.run(TOKEN)
