from app.database.database import SessionLocal

from app.repositories.state_repository import StateRepository

from app.services.gmail.gmail_service import GmailService

db = SessionLocal()

gmail = GmailService()

profile = gmail.service.users().getProfile(
    userId="me"
).execute()

history_id = profile["historyId"]

StateRepository(db).save_state(
    history_id,
    ""
)

db.close()

print("History initialized.")