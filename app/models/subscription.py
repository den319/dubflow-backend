

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base, UUIDMixin


class Subscription(Base, UUIDMixin):
    __tablename__ = "subscriptions"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    plan_type = Column(
        String,
        nullable=False,
    )

    payment_provider = Column(
        String,
        nullable=True,
    )

    provider_customer_id = Column(
        String,
        nullable=True,
    )

    provider_subscription_id = Column(
        String,
        nullable=True,
    )

    status = Column(
        String,
        nullable=False,
        default="active",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )