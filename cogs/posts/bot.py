import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext import tasks
from typing import List 
import datetime

import config 
from .core import services as services
from .core import models as models

class ScrapbookPosts(commands.Cog, name="scrapbook_posts"):
    def __init__(self, *args, **kwargs):

        self.channels = set()
        self.task_queue = {}

    @commands.command(alias="asc", strip_after_prefix=True)
    async def add_scrapbook_channel(self, ctx, channel: discord.channel.TextChannel):
        """Define a channel for Scrappy to monitor for messages

        Arguments:
            ctx -- _description_
            channel -- _description_
        """
        self.channels.add(channel)
        channel.edit(
            topic = config.TEXT.SCRAPBOOK_CHANNEL_TITLE
        )

    @commands.Cog.listener()
    async def on_message(self, ctx: Context):
        """When new messages are created, check for attachements/content"""
        
        # Check if message is in a scrappy channel
        if ctx.message.channel in self.channels:
            # Check if message has attachments/images
            if ctx.message.attachments:
                post = self.add_post_to_queue(
                    attachments = ctx.message.attachments,
                    created_at = ctx.message.created_at,
                    author = ctx.message.author.id,
                    text = ctx.message.content
                )
                await ctx.message.add_reaction("🚀")
                
                embed = discord.Embed(
                        title="Awesome!",
                        description=f"Here's our text {post.to_json()=}",
                        # We need to capitalize because the command arguments have no capital letter in the code.
                        color=0xE02B2B,
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.message.add_reaction("👀")


    @tasks.loop(seconds=config.PERSIST_POSTS_INTERVAL)
    async def persist_posts(self):
        """Persist task queue to API"""
        persisted = []
        for post in self.task_queue:
            if services.save_post(post):
                persisted.append(post.author)

        [self.task_queue.pop(author) for author in persisted]

    def add_post_to_queue(self, author, post_creator:discord.Member, attachments:List[discord.Attachment], text:str, created_at:datetime.datetime):
        new_post = models.Post(author, attachments, created_at)
        self.task_queue[author] = new_post
        return new_post
