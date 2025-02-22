from random import choice
from fastapi import APIRouter, HTTPException

from utils import create_jwt, validate_jwt
from database import jwt_to_emoji, emojis


router = APIRouter(prefix="/login", tags=["Login"])


@router.get(
    "/",
    summary="User authorization",
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

@router.get(
    '/check_token/{token:str}',
    summary='Check that the token is valid and can be used',
)
def check_token(token: str):
    if validate_jwt(token):
        return {'ok': True, 'msg': 'Correct JWT'}
    else:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})
