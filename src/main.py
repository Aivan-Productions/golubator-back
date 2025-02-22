from random import choice
import jwt
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException

from chats_views import router as chats_router
from login_views import router as login_router


app = FastAPI()
app.include_router(chats_router)
app.include_router(login_router)

load_dotenv()
SECRET_KEY_JWT = os.getenv('SECRET_KEY_JWT')
