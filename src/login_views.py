from random import choice
from fastapi import APIRouter, HTTPException

from utils import create_jwt, validate_jwt
from database import get_emoji, remove_emoji


router = APIRouter(prefix="/login", tags=["Login"])


@router.get(
    "/",
    summary="User authorization",
)
def login():
    # get random emoji (if there is), else return exception
    emoji = get_emoji()
    if emoji:
        remove_emoji(emoji)
    else:
        return HTTPException(status_code=404, detail={'msg': 'The limit of participants in the chat has been exceeded'})

    token = create_jwt({'emoji': emoji})

    return {'token': token}

@router.get(
    '/check_token/{token:str}',
    summary='Check that the token is valid and can be used',
)
def check_token(token: str):
    data = validate_jwt(token)
    if data:
        return {'ok': True, 'msg': 'Correct JWT', 'emoji': data['emoji']}
    else:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})
