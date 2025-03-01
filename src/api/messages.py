from fastapi import APIRouter, HTTPException
from datetime import datetime
from services.messages import MessagesService
from utils import validate_jwt
from schemas.messages import MessageSchemaAdd


router = APIRouter(
    prefix="/messages",
    tags=["Messages"])


@router.get(
    "",
    summary="Get message from chat by chat_slub",
)
async def get_messages():
    return await MessagesService().get_all_messages()


@router.post(
    "",
    summary="Post message in a chat",
)
async def post_message(
    message: MessageSchemaAdd
):
    # Validate jwt
    emoji = validate_jwt(message.jwt)
    
    if not emoji:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})

    # Add message to the chat
    await MessagesService().add_message({
        'text': message.text,
        'emoji': emoji['emoji'],
        'timestamp': datetime.now()
    })

    return {'ok': True, 'msg': 'Success post message'}

