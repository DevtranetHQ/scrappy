import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext import tasks
from typing import List
import datetime

import config
from .core import services as services
from .core import models as models
import servus


class ScrapbookPosts(commands.Cog, name="scrapbook_posts"):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        self.channels = set()
        self.task_queue = {}
        self.session = servus.ClientSession()

    @commands.Cog.listener()
    async def on_ready(self):
        self.persist_posts_task.start()

    @commands.command(aliases=["asc", "add_channel"], strip_after_prefix=True)
    async def add_scrapbook_channel(self, ctx, channel: discord.channel.TextChannel):
        """Define a channel for Scrappy to monitor for messages

        Arguments:
            ctx -- _description_
            channel -- _description_
        """
        self.channels.add(channel)
        await channel.edit(topic=config.TEXT.SCRAPBOOK_CHANNEL_TITLE)
        embed = discord.Embed(
            title="Awesome!",
            description=f"Now monitoring {channel.mention} for posts...",
            color=0xE02B2B,
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx: Context):
        """When new messages are created, check for attachements/content"""
        # Check if message is in a scrappy channel
        if ctx.channel in self.channels:
            # Check if message has attachments/images
            if ctx.attachments:
                post = self.add_post_to_queue(
                    attachments=ctx.attachments,
                    created_at=ctx.created_at,
                    author=ctx.author.id,
                    text=ctx.content,
                )
                await ctx.add_reaction("🚀")
                print(post.to_json())
                embed = discord.Embed(
                    title="Awesome!",
                    description=f"Here's our text {post.to_json()=}",
                    # We need to capitalize because the command arguments have no capital letter in the code.
                    color=0xE02B2B,
                )
                await ctx.channel.send(embed=embed)
            else:
                await ctx.add_reaction("👀")

    @tasks.loop(seconds=config.PERSIST_POSTS_INTERVAL)
    async def persist_posts_task(self):
        """Persist task queue to API"""
        print(f"Running Background Task {self.task_queue}")
        persisted = []
        for author, post in self.task_queue.items():
            if await services.save_post(session=self.session, post=post):
                persisted.append(post.author)

        [self.task_queue.pop(author) for author in persisted]
        print(f"Finished Background Task {self.task_queue}")
    def add_post_to_queue(
        self,
        author,
        attachments: List[discord.Attachment],
        text: str,
        created_at: datetime.datetime,
    ):
        new_post = models.Post(
            author=author, attachments=attachments, text=text, created_at=created_at
        )
        self.task_queue[author] = new_post
        return new_post

    @classmethod
    def from_db(bot_instance:discord.ext.commands.Bot):
        pass
