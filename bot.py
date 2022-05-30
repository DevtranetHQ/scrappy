import discord
from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import Context

import config


bot = Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"Discord API version: {discord.__version__}")


if __name__ == "__main__":
    bot.run(config.TOKEN)