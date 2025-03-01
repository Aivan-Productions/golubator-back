from pydantic import BaseModel, Field


class EmojiSchemaAdd(BaseModel):
    emoji: str = Field(max_length=1)


