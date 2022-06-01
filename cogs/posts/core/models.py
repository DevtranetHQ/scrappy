# Everything about Persistence
import discord
from typing import List 
import datetime 
import json

class Post:
    def __init__(self, author:int, attachments:List[discord.Attachment], text:str, created_at:datetime.datetime):
        self.author = author
        self.attachments = attachments
        self.created_at = created_at
        
    def to_json(self):
        return json.dumps({
            "discord_id":self.author,
            "attachments":self.attachments,
            "text":self.text,
            "created_at":self.created_at
        })
