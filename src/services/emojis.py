from db.database import db
from typing import List, Dict


class EmojisService:
    async def get_emoji(self) -> str:
        data = await db.emojis.find_one()
        emoji_str = data['emoji']
        return emoji_str


    async def remove_emoji(self, emoji: str) -> None:
        await db.emojis.delete_one(
            {
                'emoji': emoji
            })
