from sqlalchemy import Column, Integer, String

from app.database.base import Base


class GmailState(Base):
    __tablename__ = "gmail_state"

    id = Column(Integer, primary_key=True)

    latest_history_id = Column(
        String,
        nullable=False,
    )

    watch_expiration = Column(
        String,
        nullable=False,
    )