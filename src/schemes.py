from pydantic import BaseModel, Field


class MessageScheme(BaseModel):
    jwt: str
    text: str = Field(max_length=255)
