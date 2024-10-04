from enum import StrEnum
from typing import Literal, Optional
from pydantic import BaseModel, field_validator


class OpenAICompatibleMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class BlobType(StrEnum):
    chat = "chat"
    doc = "doc"
    image = "image"
    transcript = "transcript"


class Blob(BaseModel):
    type: BlobType
    fields: Optional[dict] = None

    def get_blob_data(self):
        return self.model_dump(exclude={"type", "fields"})


class ChatBlob(Blob):
    messages: list[OpenAICompatibleMessage]
    type: Literal[BlobType.chat] = BlobType.chat


class DocBlob(Blob):
    content: str
    type: Literal[BlobType.doc] = BlobType.doc
