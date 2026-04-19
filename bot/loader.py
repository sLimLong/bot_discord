import os

def load_extensions(bot):
    for folder in ("commands", "tasks"):
        for filename in os.listdir(folder):
            if filename.endswith(".py") and filename != "__init__.py":
                ext = f"{folder}.{filename[:-3]}"
                bot.load_extension(ext)
                print(f"Loaded: {ext}")
