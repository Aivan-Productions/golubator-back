import jwt
import os
from dotenv import load_dotenv

from database import jwt_to_emoji


load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")

def create_jwt(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY_JWT, algorithm="HS256")


def validate_jwt(token: str) -> bool:
    return token in jwt_to_emoji
