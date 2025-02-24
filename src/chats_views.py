from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import insert_message, data, get_all_messages
from utils import validate_jwt
from schemes import MessageScheme

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.get(
    "/main/",
    summary="Get message from chat by chat_slub",
)
def get_messages():
    return get_all_messages()


@router.post(
    "/main/",
    summary="Post message in a chat",
)
def post_message(message: MessageScheme):
    # Validate jwt
    emoji = validate_jwt(message.jwt)
    if not emoji:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})

    # Add message to the chat
    insert_message({
        'text': message.text,
        'emoji': emoji['emoji'],
        'timestamp': datetime.now()
    })

    return {'ok': True, 'msg': 'Success post message'}

