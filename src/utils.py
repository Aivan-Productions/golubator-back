import jwt
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")


def create_jwt(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY_JWT, algorithm="HS256")


def validate_jwt(token: str) -> bool:
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=['HS256'])
        return decoded_payload

    except jwt.InvalidTokenError:
        print('Invalid token')

    return None
