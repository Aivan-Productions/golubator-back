from random import choice
import jwt
import datetime
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

load_dotenv()
SECRET_KEY_JWT = os.getenv('SECRET_KEY_JWT')

# use as a DB for now
data = {}
# save valid JWT. {jwt: emoji}
jwt_to_emoji = {}
# available emojis
emojis = {'🤢', '😍', '👽', '🥸', '🥳', '🐵'}


class MessageScheme(BaseModel):
    jwt: str
    text: str = Field(max_length=255)


def create_jwt(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY_JWT, algorithm="HS256")


def validate_jwt(token: str) -> bool:
    return token in jwt_to_emoji


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
    # Create a chat if it doesn't exist
    if chat_slug not in data:
        data[chat_slug] = []

    # Validate jwt
    if not validate_jwt(message.jwt):
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})

    # Add message to the chat
    data[chat_slug].append({
        'jwt': message.jwt,
        'text': message.text,
        'emoji': jwt_to_emoji[message.jwt],
        'timestamp': datetime.datetime.now()
    })

    return {'ok': True, 'msg': 'Success post message'}


@app.get(
    "/login/",
    summary="User authorization",
    tags=["Chat"]
)
def login():
    # get random emoji (if there is), else return exception
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
    if validate_jwt(token):
        return {'ok': True, 'msg': 'Correct JWT'}
    else:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})
