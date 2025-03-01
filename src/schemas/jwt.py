from pydantic import BaseModel, Field


class JWTSchema(BaseModel):
    jwt: str
