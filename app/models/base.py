import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        )