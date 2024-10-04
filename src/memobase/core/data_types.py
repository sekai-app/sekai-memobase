from typing import Literal
from pydantic import BaseModel, Field
from ..utils import generate_a_uuid


class OpenAICompatibleMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Blob(BaseModel):
    id: str = Field(default_factory=generate_a_uuid)
    type: Literal["chat", "doc"]


class ChatBlob(Blob):
    messages: list[OpenAICompatibleMessage]
    type: Literal["chat"] = "chat"


class DocBlob(Blob):
    content: str
    type: Literal["doc"] = "doc"
