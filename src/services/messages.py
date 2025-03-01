from db.database import db
from schemas.messages import MessageSchemaAdd
from typing import List, Dict


class MessagesService:
    async def get_all_messages(self) -> List[Dict]:
        messages_cursor = await db.messages.find().to_list()
        messages = []
        for message in messages_cursor:
            messages.append({
                'text': message['text'],
                'emoji': message['emoji'],
                'timestamp': message['timestamp']
            })

        return messages
    
    async def add_message(self, message: MessageSchemaAdd,) -> None:
        await db.messages.insert_one(message)  
    
