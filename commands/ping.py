from discord.ext import commands

async def setup(bot):
    @bot.command(name="ping")
    async def ping_cmd(ctx):
        await ctx.send("pong")
