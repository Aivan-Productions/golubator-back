import jwt
from config import settings
from random import choice


def create_jwt(data: dict) -> str:
    return jwt.encode(data, settings.SECRET_KEY_JWT, algorithm="HS256")


def validate_jwt(token: str) -> bool:
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=['HS256'])
        return decoded_payload

    except jwt.InvalidTokenError:
        print('Invalid token')

    return None


def get_random_emoji() -> str:
    emojis = ['🤢', '😍', '👽', '🥸', '🥳', '🐵']
    return choice(emojis)
