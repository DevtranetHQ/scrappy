import discord
from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import Context

import config

import cogs.posts.bot

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = Bot(command_prefix=commands.when_mentioned_or(config.PREFIX), intents=intents)


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"Discord API version: {discord.__version__}")


@bot.command()
async def ping(ctx: Context):
    await ctx.send("Hello Beautiful World! 🚌")


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """

    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


# ADD COGS

bot.add_cog(cogs.posts.bot.ScrapbookPosts(bot))

if __name__ == "__main__":
    bot.run(config.SECRETS.DISCORD_TOKEN)
