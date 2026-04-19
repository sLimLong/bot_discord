import os

async def load_extensions(bot):
    for folder in ("commands", "tasks"):
        for filename in os.listdir(folder):
            if filename.endswith(".py") and filename != "__init__.py":
                ext = f"{folder}.{filename[:-3]}"
                await bot.load_extension(ext)
                print(f"Loaded: {ext}")
