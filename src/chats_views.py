from fastapi import APIRouter, HTTPException
from datetime import datetime

from database import data, jwt_to_emoji
from utils import validate_jwt
from schemes import MessageScheme

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.get(
    "/{chat_slug}/",
    summary="Get message from chat by chat_slub",
)
def get_messages(chat_slug: str):
    if chat_slug in data:
        return data[chat_slug]
    else:
        return HTTPException(status_code=404, detail={'msg': 'The chat was not found'})


@router.post(
    "/{chat_slug}/",
    summary="Post message in chat",
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
        'timestamp': datetime.now()
    })

    return {'ok': True, 'msg': 'Success post message'}

