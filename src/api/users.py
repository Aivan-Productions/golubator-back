from random import choice
from fastapi import APIRouter, HTTPException

from utils import create_jwt, validate_jwt
from services.emojis import EmojisService
from schemas.jwt import JWTSchema


router = APIRouter(prefix="/users",
                    tags=["Users"],
                    )


@router.get(
    "/registration",
    summary="Send the created JWT",
)
async def login():
    # get random emoji (if there is), else return exception
    emoji = await EmojisService().get_emoji()
    if emoji:
        await EmojisService().remove_emoji(emoji)
    else:
        return HTTPException(status_code=404, detail={'msg': 'The limit of participants in the chat has been exceeded'})

    jwt = create_jwt({'emoji': emoji})

    return {'JWT': jwt}


@router.post(
    '/check_jwt',
    summary='Check that the token is valid and can be used',
)
async def check_token(
    jwt: JWTSchema,
):
    data = validate_jwt(jwt.jwt)
    if data:
        return {'ok': True, 'msg': 'Correct JWT', 'emoji': data['emoji']}
    else:
        return HTTPException(status_code=404, detail={'msg': 'Incorrect JWT'})
