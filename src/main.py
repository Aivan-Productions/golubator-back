from hashlib import algorithms_available
from typing import List
from random import choice
import uvicorn
import jwt
import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

SECRET_KEY = 'secret key'

# типо BD
data = {}
# хэш таблица, в котором хранятся валидные токены. {jwt: emoji}
jwt_to_emoji = {}
# доступные эмодзи
emojis = {'🤢', '😍', '👽', '🥸', '🥳', '🐵'}


class MessageScheme(BaseModel):
    jwt: str
    text: str = Field(max_length=255)


def create_jwt(data: dict) -> str:
    """Генерируем JWT"""
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def validate_jwt(token: str):
    """Просто проверка, что jwt есть в jwt_to_emoji и пользователь может отправлять сообщения, используя его"""
    return token in jwt_to_emoji


@app.get(
    "/chats/{chat_slug}/",
    summary="Get message from chat by chat_slub",
    tags=["Chat"]
)
def get_messages(chat_slug: str):
    """Получаем все сообщения из чата с определенным slug"""
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

    # Валидация jwt
    if not validate_jwt(message.jwt):
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})

    # Добавляем сообщение в чат
    data[chat_slug].append({
        'jwt': message.jwt,
        'text': message.text,
        'emoji': jwt_to_emoji[message.jwt],
        'timestamp': datetime.datetime.now()
    })

    return {'ok': True, 'msg': 'Success post message'}


@app.get(
    "/login/",
    summary="Login",
    tags=["Chat"]
)
def login():
    """авторизация пользователя. Выдается личный JWT"""
    # получаем рандомно emoji (если еще остались) из emojis. Иначе возвращаем нет доступа
    if emojis:
        emoji = choice(list(emojis))
        emojis.remove(emoji)
    else:
        return HTTPException(status_code=404, detail={'msg': 'The limit of participants in the chat has been exceeded'})

    token = create_jwt({'emoji': emoji})
    jwt_to_emoji[token] = emoji

    return {'token': token}

@app.get(
    '/check_token/{token:str}',
    summary='Check that the token is valid and can be used',
    tags=['Chat'],
)
def check_token(token: str):
    """Проверка валидности токена"""
    if validate_jwt(token):
        return {'ok': True, 'msg': 'Correct JWT'}
    else:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
