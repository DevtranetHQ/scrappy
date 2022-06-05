# Everything about Persistence
import discord
from typing import List
import datetime
import json


class Post:
    def __init__(
        self,
        author: int,
        attachments: List[discord.Attachment],
        text: str,
        created_at: datetime.datetime,
    ):
        self.author = author
        self.attachments = attachments
        self.created_at = created_at
        self.text = text

    def to_json(self):
        print(self.attachments)
        # """[<Attachment id=982884678157619220 filename='arab_logo.png' url='https://cdn.discordapp.com/attachments/935673679801643020/982884678157619220/arab_logo.png'>]"""
        attachments = self.__serialize_attachments()
        return json.dumps(
            {
                "discord_id": self.author,
                "attachments": attachments,
                "text": self.text,
                "created_at": self.created_at.isoformat(),
            }
        )

    def __serialize_attachments(self):
        return [
            dict(id=attachment.id, filename=attachment.filename, url=attachment.url)
            for attachment in self.attachments
        ]
