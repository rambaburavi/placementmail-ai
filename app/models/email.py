from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from app.database.base import Base


class Email(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)

    gmail_message_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    thread_id = Column(String)

    sender = Column(String)

    subject = Column(String)

    body = Column(Text)

    category = Column(String)

    priority = Column(String)

    placement_related = Column(Boolean)

    company = Column(String)

    deadline = Column(String)

    action_required = Column(Text)

    summary = Column(Text)
    
    ai_provider = Column(String)

    analysis_status = Column(String)

    created_at = Column(
    DateTime,
    default=datetime.utcnow,
    nullable=False,
    )

    deadline_at = Column(DateTime)

    # Relationship to EmailReminder
    reminders = relationship(
        "EmailReminder",
        back_populates="email",
        cascade="all, delete-orphan",
    )

    reminder_24_sent = Column(
        Boolean,
        default=False,
    )

    reminder_12_sent = Column(
        Boolean,
        default=False,
    )

    reminder_6_sent = Column(
        Boolean,
        default=False,
    )

    reminder_1_sent = Column(
        Boolean,
        default=False,
    )

    reminder_15_sent = Column(
        Boolean,
        default=False,
    )