from db.database import mongodb
from typing import List, Dict


class EmojisService:
    async def get_emoji(self) -> str:
        data = await mongodb.get_collection('emojis').find_one()
        emoji_str = data['emoji']
        return emoji_str


    async def remove_emoji(self, emoji: str) -> None:
        await mongodb.get_collection('emojis').delete_one(
            {
                'emoji': emoji
            })
