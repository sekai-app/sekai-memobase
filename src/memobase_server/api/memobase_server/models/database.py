from typing import Optional
from datetime import datetime
from sqlalchemy import (
    CHAR,
    Integer,
    ForeignKey,
    TIMESTAMP,
)
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    registry,
)
from sqlalchemy.sql import func
from .blob import BlobType

REG = registry()


@dataclass
class Base:
    __abstract__ = True  # 这个属性表示这是一个抽象基类，不会创建对应的表

    # Common columns
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), init=False
    )
    addional_fields: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, default=None, init=False
    )


@REG.mapped_as_dataclass
class User(Base):
    __tablename__ = "users"

    # Relationships
    general_blobs: Mapped[list["GeneralBlob"]] = relationship(
        "GeneralBlob", back_populates="user", init=False
    )


@REG.mapped_as_dataclass
class GeneralBlob(Base):
    __tablename__ = "general_blobs"

    # Specific columns
    blob_type: Mapped[str] = mapped_column(CHAR(255), nullable=False)
    blob_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Relationships
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship("User", back_populates="chat_blobs", init=False)

    # validate
    def __post_init__(self):
        assert self.type in BlobType, f"Invalid blob type: {self.type}"
