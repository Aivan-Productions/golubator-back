from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

data = {}

class MessageScheme(BaseModel):
    text: str = Field(max_length=100)
    author: str = Field(max_length=50)


@app.get(
    "/chats/{chat_slug}/",
    summary="Get message from chat by chat_slub",
    tags=["Chat"]
)
def get_messages(chat_slug: str):
    if chat_slug in data:
        return data[chat_slug]
    else:
        return HTTPException(status_code=404, detail={'msg': 'The chat was not found'})


@app.post(
    "/chats/{chat_slug}/",
    summary="Post message in chat",
    tags=["Chat"]
)
def post_message(chat_slug: str, message: MessageScheme):
    # Создаем чат(комнату) если его не было
    if chat_slug not in data:
        data[chat_slug] = []

    # Добавляем сообщение в чат
    data[chat_slug].append({
        'id': len(data[chat_slug]) + 1,
        'text': message.text,
        'author': message.author,
    })

    return {'ok': True, 'msg': 'Success post message'}

