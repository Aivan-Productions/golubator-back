from pydantic import BaseModel, Field


class MessageSchemaAdd(BaseModel):
    jwt: str
    text: str = Field(min_length=1, max_length=255)

