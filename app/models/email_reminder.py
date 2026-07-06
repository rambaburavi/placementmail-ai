from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database.base import Base


class EmailReminder(Base):
    __tablename__ = "email_reminders"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(
        Integer,
        ForeignKey("emails.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_id = Column(String, unique=True, nullable=False, index=True)

    offset_minutes = Column(Integer, nullable=False)

    reminder_time = Column(DateTime, nullable=False, index=True)

    status = Column(String, default="PENDING", nullable=False)

    sent_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)

    email = relationship("Email", back_populates="reminders")