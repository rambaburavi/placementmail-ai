from app.database.base import Base
from app.database.database import engine

# Import ALL models here
from app.models.email import Email
from app.models.gmail_state import GmailState
from app.models.email_reminder import EmailReminder

def init_db():
    Base.metadata.create_all(bind=engine)