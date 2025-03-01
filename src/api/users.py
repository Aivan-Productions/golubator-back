from random import choice
from fastapi import APIRouter, HTTPException

from utils import create_jwt, validate_jwt
from utils import get_random_emoji
from schemas.jwt import JWTSchema


router = APIRouter(prefix="/users",
                    tags=["Users"],
                    )


@router.get(
    "/registration",
    summary="Send the created JWT",
)
async def login():
    emoji = get_random_emoji()

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
